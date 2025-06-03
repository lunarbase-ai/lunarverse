import pandas as pd
import numpy as np
import pingouin as pg
import seaborn as sns
import os
from datetime import datetime
import matplotlib.pyplot as plt


# ----------------------------
# Base class with universal methods.
# ----------------------------
class LRPComparisonBase:
    """
    Base class containing universal methods used by all subclasses:
    - Data rounding and exporting
    - Selecting top N features
    - Shared utilities for handling path creation, etc.
    """
    def __init__(
        self, data_df, clinical_features_df, data_level="node", path_to_save=None
    ):
        """
        Initialize the base class with data, clinical features, data level, and save path.

        Parameters:
            data_df (pd.DataFrame): DataFrame containing LRP values.
            clinical_features_df (pd.DataFrame): DataFrame containing clinical features.
            data_level (str): Indicates the data level, either 'node' or 'edge'.
            path_to_save (str, optional): Directory where results are saved.
        """
        self.data_level = data_level.lower()
        self.lrp = data_df
        # Auto-detect data level based on column names
        if all(len(col.split(" - ")) == 2 for col in self.lrp.columns):
            if self.data_level != "edge":
                self.data_level = "edge"
                print(
                    "\nINFO: data_level automatically set to 'edge' based on column names.\n"
                )
        else:
            if self.data_level == "edge":
                self.data_level = "node"
                print(
                    "\nINFO: data_level automatically set to 'node' based on column names.\n"
                )
        self.clinical_features = clinical_features_df
        # Create path_to_save folder if needed
        if path_to_save is None:
            # Fix: Use current working directory as base path instead of undefined 'path' variable
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.path_to_save = os.path.join(
                os.getcwd(), f"LRP_comparison_results_{current_time}"
            )
            if not os.path.exists(self.path_to_save):
                os.makedirs(self.path_to_save)
        else:
            self.path_to_save = path_to_save
            # Create the directory if it doesn't exist
            if not os.path.exists(self.path_to_save):
                os.makedirs(self.path_to_save)

        # Print heads for inspection
        print("lrp.head():\n", self.lrp.head())
        print("clinical_features.head():\n", self.clinical_features.head())

    def round_boxplot_values(self):
        """
        Round all numeric columns in self.boxplot_df (except 'p-value') to 4 decimal places.
        """
        self.boxplot_df = self.boxplot_df.round(
            {col: 4 for col in self.boxplot_df.columns if col != "p-value"}
        )

    def select_top_n_by_column(self, column="p-value", n=5, ascending=True):
        """
        Select top N rows of self.boxplot_df grouped by 'type', ordered by the given column.

        Parameters:
            column (str): Column to sort by (e.g., 'p-value').
            n (int): Number of top rows to select per group.
            ascending (bool): Sort order.

        Returns:
            pd.DataFrame: The resulting top N subset.
        """
        sort_by = ["type", column]
        df_sorted = self.boxplot_df.sort_values(by=sort_by, ascending=ascending)
        self.top_n_df = df_sorted.groupby("type").head(n)
        self.n = n
        return self.top_n_df

    def save_boxplot_to_csv(self):
        """
        Save self.boxplot_df to a CSV file in path_to_save.
        """
        filename = f"boxplot_df.csv"
        full_path = os.path.join(self.path_to_save, filename)
        self.boxplot_df.to_csv(full_path)
        print(f"Boxplot DataFrame saved to: {full_path}")

    def save_top_n_to_csv(self):
        """
        Save the top N subset DataFrame (self.top_n_df) to a CSV file in path_to_save.
        """
        filename = f"top_n_df_top{self.n}.csv"
        full_path = os.path.join(self.path_to_save, filename)
        self.top_n_df.to_csv(full_path)
        print(f"Top N DataFrame saved to: {full_path}")

    def save_top_n_by_type(self):
        """
        For each unique 'type' in the top N subset, save a separate CSV.
        """
        types = self.top_n_df["type"].unique()
        for t in types:
            t_df = self.top_n_df[self.top_n_df["type"] == t]
            filename = f"top_n_df_top{self.n}_{t}.csv"
            full_path = os.path.join(self.path_to_save, filename)
            t_df.to_csv(full_path)
            print(f"Top N DataFrame for type '{t}' saved to: {full_path}")

    def format_median_diff(self, diff):
        """
        Format the median difference for display in the plot annotation.

        Parameters:
            diff (float): The median difference value.

        Returns:
            str: Formatted median difference as string.
        """
        if abs(diff) < 0.001:
            return f"{diff:.2e}"
        elif abs(diff) < 0.01:
            return f"{diff:.3f}"
        elif abs(diff) < 0.1:
            return f"{diff:.2f}"
        else:
            return f"{diff:.2f}"

    # Note: compute_boxplot_values, filter/merge and plotting methods are meant to be implemented in subclasses.


# ----------------------------
# Subclass for group_vs_group comparisons.
# ----------------------------
class GroupVsGroupComparison(LRPComparisonBase):
    """
    Perform group-versus-group comparisons based on a clinical feature column.
    """
    def __init__(self, column_name, group1_name, group2_name, **kwargs):
        """
        Initialize GroupVsGroupComparison with the target column and group labels.

        Parameters:
            column_name (str): Clinical feature column used to define the groups.
            group1_name (str): Name of the first group.
            group2_name (str): Name of the second group.
        """
        super().__init__(**kwargs)
        self.column_name = column_name
        self.group1_name = group1_name
        self.group2_name = group2_name

    def compute_boxplot_values(self):
        """
        Compute boxplot statistics (min, q1, median, q3, max) and MWU test results
        for each column in LRP data, grouping by column_name.
        Returns a DataFrame stored in self.boxplot_df.
        """
        merged_df = self.lrp.merge(
            self.clinical_features[[self.column_name]],
            left_index=True,
            right_index=True,
        )
        if self.lrp.shape[0] != self.clinical_features.shape[0]:
            raise ValueError("Row count mismatch.")
        boxplot_values = {}
        # Get group indices
        group1_mask = merged_df[self.column_name] == self.group1_name
        group2_mask = merged_df[self.column_name] == self.group2_name

        # Extract LRP values for both groups
        group1_values = merged_df.loc[group1_mask, self.lrp.columns].values
        group2_values = merged_df.loc[group2_mask, self.lrp.columns].values

        # Calculate statistics for all columns at once
        group1_min = np.min(group1_values, axis=0)
        group1_q1 = np.percentile(group1_values, 25, axis=0)
        group1_median = np.median(group1_values, axis=0)
        group1_q3 = np.percentile(group1_values, 75, axis=0)
        group1_max = np.max(group1_values, axis=0)

        group2_min = np.min(group2_values, axis=0)
        group2_q1 = np.percentile(group2_values, 25, axis=0)
        group2_median = np.median(group2_values, axis=0)
        group2_q3 = np.percentile(group2_values, 75, axis=0)
        group2_max = np.max(group2_values, axis=0)

        median_diffs = group2_median - group1_median

        # Still need to iterate for MWU tests as they require separate calls
        mwu_results = {}
        for i, col in enumerate(self.lrp.columns):
            mwu_res = pg.mwu(
                merged_df.loc[group1_mask, col], merged_df.loc[group2_mask, col]
            )[["p-val", "CLES"]]
            mwu_results[col] = {
                "p-value": mwu_res["p-val"].values[0],
                "CLES": mwu_res["CLES"].values[0],
            }

        # Build the boxplot dataframe directly
        self.boxplot_df = pd.DataFrame(
            {
                f"{self.group1_name}_min": group1_min,
                f"{self.group1_name}_q1": group1_q1,
                f"{self.group1_name}_median": group1_median,
                f"{self.group1_name}_q3": group1_q3,
                f"{self.group1_name}_max": group1_max,
                f"{self.group2_name}_min": group2_min,
                f"{self.group2_name}_q1": group2_q1,
                f"{self.group2_name}_median": group2_median,
                f"{self.group2_name}_q3": group2_q3,
                f"{self.group2_name}_max": group2_max,
                "median_diff": median_diffs,
                "p-value": [mwu_results[col]["p-value"] for col in self.lrp.columns],
                "CLES": [mwu_results[col]["CLES"] for col in self.lrp.columns],
            },
            index=self.lrp.columns,
        )

        self.boxplot_df["median_abs_diff"] = self.boxplot_df["median_diff"].abs()
        if self.data_level == "node":
            self.boxplot_df["type"] = self.boxplot_df.index.str.rsplit("_", n=1).str[1]
        elif self.data_level == "edge":
            split_edges = self.boxplot_df.index.to_series().str.split(" - ")
            source_type = split_edges.apply(
                lambda x: (
                    x[0].rsplit("_", 1)[1] if len(x[0].rsplit("_", 1)) > 1 else np.nan
                )
            )
            target_type = split_edges.apply(
                lambda x: (
                    x[1].rsplit("_", 1)[1]
                    if len(x) > 1 and len(x[1].rsplit("_", 1)) > 1
                    else np.nan
                )
            )
            self.boxplot_df["type"] = source_type.combine(
                target_type, lambda s, t: f"{t}-{s}" if s > t else f"{s}-{t}"
            )
        else:
            raise ValueError("Invalid data level.")
        self.round_boxplot_values()
        return self.boxplot_df

    def filter_and_merge_data(self, selected_type):
        """
        Merge LRP data with clinical features, then filter rows by group labels
        and columns by selected 'type'.
        """
        merged = self.lrp.merge(
            self.clinical_features[[self.column_name]],
            left_index=True,
            right_index=True,
        )
        merged = merged[
            merged[self.column_name].isin([self.group1_name, self.group2_name])
        ]
        # Filter based on selected type.
        selected_df = self.top_n_df[self.top_n_df["type"].str.contains(selected_type)]
        lrp_selected = self.lrp[selected_df.index]
        merged = lrp_selected.merge(
            self.clinical_features[[self.column_name]],
            left_index=True,
            right_index=True,
        )
        return merged

    def plot_violin(
        self,
        merged,
        selected_type,
        sort_by="median_abs_diff",
        plot_title=None,
        save_plot=False,
    ):
        """
        Plot a violin plot of the top N selected features for the specified 'type'.

        Parameters:
            merged (pd.DataFrame): Merged data to plot.
            selected_type (str): Filter type used for top N selection.
            sort_by (str): Sorting column name for display order.
            plot_title (str, optional): Title of the plot.
            save_plot (bool): Whether to save plots to files.
        """
        melted = merged.melt(
            id_vars=[self.column_name], var_name="feature", value_name="LRP"
        )
        selected_df = self.top_n_df[self.top_n_df["type"].str.contains(selected_type)]
        order = selected_df.sort_values(sort_by, ascending=False).index
        fig, ax = plt.subplots(figsize=(6, 2 + len(order) / 2))
        sns.violinplot(
            data=melted,
            y="feature",
            x="LRP",
            hue=self.column_name,
            split=True,
            inner="quart",
            palette="muted",
            dodge=True,
            order=order,
            ax=ax,
        )
        if self.data_level == "node":
            ax.set_yticklabels([label.rsplit("_", 1)[0] for label in order])
            ax.set_xlabel("$LRP_{sum}$")
        else:
            ax.set_xlabel("$LRP$")
        if plot_title is None:
            plot_title = f"{selected_type}"
        ax.set_title(plot_title)
        for i, feature in enumerate(order):
            row_data = self.top_n_df.loc[feature]
            p_val = row_data["p-value"]
            cles = row_data["CLES"]
            median_diff = row_data["median_diff"]
            x_max = ax.get_xlim()[1]  # Get the maximum x-axis value
            ax.text(
                x_max * 0.9,
                i + 0.2,
                f"p={p_val:.2e}\nCLES={cles:.2f}\nmedian_diff="
                + self.format_median_diff(median_diff),
                ha="right",
                va="bottom",
                rotation=0,
            )
        ax.set_ylabel(None)
        plt.legend(title=None, bbox_to_anchor=(0.5, -0.09), loc="upper center", ncols=2)
        plt.tight_layout()
        if save_plot:
            path_to_save_plots = os.path.join(self.path_to_save, "plots")
            if not os.path.exists(path_to_save_plots):
                os.makedirs(path_to_save_plots)
            fig.savefig(
                os.path.join(
                    path_to_save_plots,
                    f"violin_{selected_type}_{self.group1_name}_vs_{self.group2_name}.png",
                ),
                bbox_inches="tight",
            )
            fig.savefig(
                os.path.join(
                    path_to_save_plots,
                    f"violin_{selected_type}_{self.group1_name}_vs_{self.group2_name}.pdf",
                ),
                bbox_inches="tight",
                format="pdf",
            )
            print(f"Violin plot saved to: {path_to_save_plots}")


# ----------------------------
# Subclass for sample_vs_sample comparisons.
# ----------------------------
class SampleVsSampleComparison(LRPComparisonBase):
    """
    Compare LRP values for two individual samples.
    """
    def __init__(self, sample1_name, sample2_name, **kwargs):
        """
        Parameters:
            sample1_name (str): Name of the first sample.
            sample2_name (str): Name of the second sample.
        """
        super().__init__(**kwargs)
        self.sample1_name = sample1_name
        self.sample2_name = sample2_name

    def compute_boxplot_values(self):
        """
        Compute statistics for each column by retrieving LRP values for the
        two specified samples. Stores the result in self.boxplot_df.
        """
        boxplot_values = {}
        for col in self.lrp.columns:
            sample1_value = self.lrp.loc[self.sample1_name, col]
            sample2_value = self.lrp.loc[self.sample2_name, col]
            boxplot_values[col] = {
                f"{self.sample1_name}_value": sample1_value,
                f"{self.sample2_name}_value": sample2_value,
                "p-value": np.nan,
                "CLES": np.nan,
                "median_diff": sample2_value - sample1_value,
            }
        self.boxplot_df = pd.DataFrame(boxplot_values).T
        self.boxplot_df["median_abs_diff"] = self.boxplot_df["median_diff"].abs()
        if self.data_level == "node":
            self.boxplot_df["type"] = self.boxplot_df.index.str.rsplit("_", n=1).str[1]
        elif self.data_level == "edge":
            split_edges = self.boxplot_df.index.to_series().str.split(" - ")
            source_type = split_edges.apply(
                lambda x: (
                    x[0].rsplit("_", 1)[1] if len(x[0].rsplit("_", 1)) > 1 else np.nan
                )
            )
            target_type = split_edges.apply(
                lambda x: (
                    x[1].rsplit("_", 1)[1]
                    if len(x) > 1 and len(x[1].rsplit("_", 1)) > 1
                    else np.nan
                )
            )
            self.boxplot_df["type"] = source_type.combine(
                target_type, lambda s, t: f"{t}-{s}" if s > t else f"{s}-{t}"
            )
        else:
            raise ValueError("Invalid data level.")
        self.round_boxplot_values()
        return self.boxplot_df

    def filter_and_merge_data(self, selected_type):
        """
        Return the subset of self.lrp limited to the two samples and the
        selected features, based on top_n_df.
        """
        selected_df = self.top_n_df[self.top_n_df["type"].str.contains(selected_type)]
        return self.lrp.loc[[self.sample1_name, self.sample2_name]][selected_df.index]

    def plot_scatter(self, selected_type, sort_by="median_abs_diff", plot_title=None, save_plot=False):
        """
        Plot a scatter-like comparison of LRP values between the two samples.
    
        Parameters:
            selected_type (str): Filter type used for top N selection.
            sort_by (str): Sorting column name for display order.
            plot_title (str, optional): Title of the plot.
            save_plot (bool): Whether to save plots to files.
    
        Returns:
            fig: Matplotlib Figure object.
        """
        # Filter features based on the selected type and sort them.
        selected_df = self.top_n_df[self.top_n_df["type"].str.contains(selected_type)]
        order = selected_df.sort_values(sort_by, ascending=True).index

        # Create a new figure explicitly.
        fig, ax = plt.subplots(figsize=(6, 2 + len(order) / 2))
        sample1_vals = []
        sample2_vals = []
        ypos = []
        max_val = 0

        # Loop through features and prepare data.
        for idx, feat in enumerate(order):
            val1 = self.lrp.loc[self.sample1_name, feat]
            val2 = self.lrp.loc[self.sample2_name, feat]
            sample1_vals.append(val1)
            sample2_vals.append(val2)
            ypos.append(idx)
            max_val = max(max_val, val1, val2)

        # Draw connecting lines and display median difference for each feature.
        for i, (val1, val2, y) in enumerate(zip(sample1_vals, sample2_vals, ypos)):
            ax.plot([val1, val2], [y, y], color="gray", linestyle="-", linewidth=0.5, zorder=5)
            diff = self.boxplot_df.loc[order[i], "median_diff"]
            mid_x = (val1 + val2) / 2
            ax.text(mid_x, y + 0.2, f"{self.format_median_diff(diff)}", ha="center", va="bottom", fontsize=8)

        # Plot sample points.
        ax.scatter(sample1_vals, ypos, color="blue", s=50, label=self.sample1_name, marker="o", zorder=10)
        ax.scatter(sample2_vals, ypos, color="green", s=50, label=self.sample2_name, marker="s", zorder=10)

        ax.set_yticks(ypos)
        if self.data_level == "node":
            ax.set_yticklabels([label.rsplit("_", 1)[0] for label in order])
            ax.set_xlabel("$LRP_{sum}$")
        else:
            ax.set_yticklabels(order)
            ax.set_xlabel("$LRP$")

        if plot_title is None:
            plot_title = f"Sample vs Sample: {selected_type}"
        ax.set_title(plot_title)
        ax.set_ylabel(None)
        ax.set_xlim([0, None])
        plt.legend(title=None, bbox_to_anchor=(0.5, -0.05), loc="upper center", ncols=2)
        plt.tight_layout()

        if save_plot:
            path_to_save_plots = os.path.join(self.path_to_save, "plots")
            if not os.path.exists(path_to_save_plots):
                os.makedirs(path_to_save_plots)
            fig.savefig(
                os.path.join(
                    path_to_save_plots,
                    f"scatter_{selected_type}_{self.sample1_name}_vs_{self.sample2_name}.png",
                ),
                bbox_inches="tight",
            )
            fig.savefig(
                os.path.join(
                    path_to_save_plots,
                    f"scatter_{selected_type}_{self.sample1_name}_vs_{self.sample2_name}.pdf",
                ),
                bbox_inches="tight",
                format="pdf",
            )
            print(f"Scatter plot saved to: {path_to_save_plots}")

        return fig

# ----------------------------
# Subclass for sample_vs_group comparisons.
# ----------------------------
class SampleVsGroupComparison(LRPComparisonBase):
    """
    Compare one sample's LRP values to those of a group defined by a clinical feature.
    """
    def __init__(self, sample1_name, column_name, group1_name, **kwargs):
        """
        Parameters:
            sample1_name (str): Name of the sample to compare.
            column_name (str): Clinical feature column used to define the group.
            group1_name (str): Name of the group in the clinical data.
        """
        super().__init__(**kwargs)
        self.sample1_name = sample1_name
        self.column_name = column_name
        self.group1_name = group1_name

    def compute_boxplot_values(self):
        """
        Compute boxplot-like statistics for the chosen group, compare them to a
        single sample's values, then store the result in self.boxplot_df.
        """
        merged_df = self.lrp.merge(
            self.clinical_features[[self.column_name]],
            left_index=True,
            right_index=True,
        )
        group_df = merged_df[merged_df[self.column_name] == self.group1_name]
        sample_value = self.lrp.loc[self.sample1_name]

        # Vectorized calculations for group statistics.
        group_min = group_df[self.lrp.columns].min()
        group_q1 = group_df[self.lrp.columns].quantile(0.25)
        group_median = group_df[self.lrp.columns].median()
        group_q3 = group_df[self.lrp.columns].quantile(0.75)
        group_max = group_df[self.lrp.columns].max()
        median_diff = sample_value - group_median

        # Directly create the boxplot DataFrame.
        self.boxplot_df = pd.DataFrame(
            {
                f"{self.group1_name}_min": group_min,
                f"{self.group1_name}_q1": group_q1,
                f"{self.group1_name}_median": group_median,
                f"{self.group1_name}_q3": group_q3,
                f"{self.group1_name}_max": group_max,
                f"{self.sample1_name}_median": sample_value,
                "p-value": np.nan,
                "CLES": np.nan,
                "median_diff": median_diff,
            }
        )

        self.boxplot_df["median_abs_diff"] = self.boxplot_df["median_diff"].abs()
        if self.data_level == "node":
            self.boxplot_df["type"] = self.boxplot_df.index.str.rsplit("_", n=1).str[1]
        elif self.data_level == "edge":
            split_edges = self.boxplot_df.index.to_series().str.split(" - ")
            source_type = split_edges.apply(
                lambda x: (
                    x[0].rsplit("_", 1)[1] if len(x[0].rsplit("_", 1)) > 1 else np.nan
                )
            )
            target_type = split_edges.apply(
                lambda x: (
                    x[1].rsplit("_", 1)[1]
                    if len(x) > 1 and len(x[1].rsplit("_", 1)) > 1
                    else np.nan
                )
            )
            self.boxplot_df["type"] = source_type.combine(
                target_type, lambda s, t: f"{t}-{s}" if s > t else f"{s}-{t}"
            )
        else:
            raise ValueError("Invalid data level.")
        self.round_boxplot_values()
        return self.boxplot_df

    def filter_and_merge_data(self, selected_type):
        """
        Filter and merge LRP data with clinical features. Return the subset that
        contains only the specified group and the chosen sample.
        """
        selected_df = self.top_n_df[self.top_n_df["type"].str.contains(selected_type)]
        lrp_selected = self.lrp[selected_df.index]
        merged = lrp_selected.merge(
            self.clinical_features[[self.column_name]],
            left_index=True,
            right_index=True,
            how="left",
        )
        group_rows = merged[merged[self.column_name] == self.group1_name]
        sample_row = lrp_selected.loc[[self.sample1_name]]
        if self.sample1_name in self.clinical_features.index:
            sample_row = sample_row.merge(
                self.clinical_features[[self.column_name]],
                left_index=True,
                right_index=True,
            )
        merged = pd.concat([group_rows, sample_row], axis=0)
        return merged

    def plot_violin_sample_vs_group(
        self,
        merged,
        selected_type,
        sort_by="median_abs_diff",
        plot_title=None,
        save_plot=False,
    ):
        """
        Plot a violin plot to compare a single sample's distribution of LRP values
        against a group's distribution for selected features.

        Parameters:
            merged (pd.DataFrame): Merged data to plot.
            selected_type (str): Filter type used for top N selection.
            sort_by (str): Sorting column name for display order.
            plot_title (str, optional): Title of the plot.
            save_plot (bool): Whether to save plots to files.
        """
        melted_group = merged[merged[self.column_name] == self.group1_name].melt(
            id_vars=[self.column_name], var_name="feature", value_name="LRP"
        )
        melted_sample = merged.loc[[self.sample1_name]].melt(
            id_vars=[self.column_name], var_name="feature", value_name="LRP"
        )
        selected_df = self.top_n_df[self.top_n_df["type"].str.contains(selected_type)]
        order = selected_df.sort_values(sort_by, ascending=False).index
        fig, ax = plt.subplots(figsize=(6, 2 + len(order) / 2))
        sns.violinplot(
            data=melted_group,
            y="feature",
            x="LRP",
            hue=self.column_name,
            split=True,
            inner="quart",
            palette="muted",
            dodge=True,
            order=order,
            ax=ax,
        )
        max_lrps = []
        for idx, feat in enumerate(order):
            sample_vals = melted_sample[melted_sample["feature"] == feat]["LRP"]
            max_lrps.append(sample_vals.max())
            if not sample_vals.empty:
                ax.scatter(
                    sample_vals.values[0],
                    idx,
                    color="red",
                    zorder=10,
                    label=self.sample1_name if idx == 0 else "",
                )
        max_lrp = max(max_lrps)
        if self.data_level == "node":
            ax.set_xlabel("$LRP_{sum}$")
        else:
            ax.set_xlabel("$LRP$")
        for i, row in enumerate(self.top_n_df.loc[order].itertuples()):
            diff = row.median_diff
            ax.text(
                max_lrp * 1.1,
                i + 0.2,
                f"median_diff={self.format_median_diff(diff)}",
                ha="left",
                va="bottom",
                rotation=0,
            )
        ax.set_ylabel(None)
        if plot_title is None:
            plot_title = f"{selected_type}"
        ax.set_title(plot_title)
        plt.legend(title=None, bbox_to_anchor=(0.5, -0.05), loc="upper center", ncols=2)
        plt.tight_layout()
        if save_plot:
            path_to_save_plots = os.path.join(self.path_to_save, "plots")
            if not os.path.exists(path_to_save_plots):
                os.makedirs(path_to_save_plots)
            fig.savefig(
                os.path.join(
                    path_to_save_plots,
                    f"violin_sample_vs_group_{selected_type}_{self.group1_name}_{self.sample1_name}.png",
                ),
                bbox_inches="tight",
            )
            fig.savefig(
                os.path.join(
                    path_to_save_plots,
                    f"violin_sample_vs_group_{selected_type}_{self.group1_name}_{self.sample1_name}.pdf",
                ),
                bbox_inches="tight",
                format="pdf",
            )
            print(f"Violin plot saved to: {path_to_save_plots}")
