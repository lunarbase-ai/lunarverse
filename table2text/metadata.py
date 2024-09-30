# SPDX-FileCopyrightText: Copyright © 2024 Eliezer Silva <djosacv@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import spacy


class TableMetadata:
    def __init__(self, table, nlp_model: str = "en_core_web_sm", verbose=False):
        # Drop duplicate columns
        table = table.T.drop_duplicates().T
        self.columns = table.columns
        self.rows = table.index
        self.metadata = dict()
        self.data = table

        if not spacy.util.is_package(nlp_model):
            spacy.cli.download(nlp_model)

        self._nlp_model = spacy.load(nlp_model)

        self.VERBOSE = verbose

    @property
    def nlp_model(self):
        return self._nlp_model

    def __linking_predicate__(
        self,
        is_number,
        is_plural=False,
        is_date=False,
        is_long_text=False,
        most_common_spacy_tag=None,
    ):
        if most_common_spacy_tag is not None:
            if most_common_spacy_tag == "DATE" or most_common_spacy_tag == "TIME":
                return "on the date of"
            if (
                most_common_spacy_tag == "GPE"
                or most_common_spacy_tag == "LOC"
                or most_common_spacy_tag == "FAC"
            ):
                return "in"
            if most_common_spacy_tag == "PERSON":
                return "is"
            if most_common_spacy_tag == "ORG":
                return "is"
            if most_common_spacy_tag == "EVENT":
                return "is"
            if most_common_spacy_tag == "NORP":
                return "is"
            if most_common_spacy_tag == "PRODUCT":
                return "is"
            if most_common_spacy_tag == "WORK_OF_ART":
                return "is"
            if most_common_spacy_tag == "LAW":
                return "is"
            if most_common_spacy_tag == "LANGUAGE":
                return "is"
            if most_common_spacy_tag == "PERCENT":
                return "is"
            if most_common_spacy_tag == "MONEY":
                return "is"
            if most_common_spacy_tag == "QUANTITY":
                return "has"
            if most_common_spacy_tag == "ORDINAL":
                return "is"
        if is_long_text:
            return "with"

        if is_number:
            if is_plural:
                return "have"
            else:
                return "has"
        else:
            if is_date:
                return "on the date of"
            if is_plural:
                return "are"
            else:
                return "is"

    def __include__colname__in__phrase__(self, col_name: str, linking_predicate: str):
        # check if the column name should be included in the phrase by type of linking predicate and most common spacy tag
        if linking_predicate in ["have", "has"]:
            return True
        if col_name in self.metadata:
            # check most common spacy tag
            most_common_spacy_tag = self.metadata[col_name]["most_common_spacy_tag"]
            if most_common_spacy_tag == "QUANTITY":
                return True
            if most_common_spacy_tag == "ORDINAL":
                return True
            if most_common_spacy_tag == "PERCENT":
                return True
            if most_common_spacy_tag == "MONEY":
                return True
            if most_common_spacy_tag == "CARDINAL":
                return True
            if most_common_spacy_tag == "DATE":
                return True
            if most_common_spacy_tag == "TIME":
                return True
            if most_common_spacy_tag == "NUM":
                return True
            if most_common_spacy_tag == "CD":
                return True
        return False

    def __process__column__tags__(self, col_name: str):
        # get column data from pandas
        col = self.data[col_name]
        # calculate spacy tag for each element in the column
        spacy_tags = dict()
        for d in col:
            spacy_tags[d] = (
                self._nlp_model(str(d)).ents[0].label_
                if len(self._nlp_model(str(d)).ents) > 0
                else self._nlp_model(str(d))[0].tag_
            )
        # calculate the most common spacy tag
        spacy_tag_count = dict()
        for d in col:
            tag = spacy_tags[d]
            if tag not in spacy_tag_count:
                spacy_tag_count[tag] = 0
            spacy_tag_count[tag] += 1
        most_common_spacy_tag = max(spacy_tag_count, key=spacy_tag_count.get)
        # calculate the ratio of the most common spacy tag
        most_common_spacy_tag_ratio = spacy_tag_count[most_common_spacy_tag] / len(col)
        # return the most common spacy tag and its ratio
        return most_common_spacy_tag, most_common_spacy_tag_ratio, spacy_tag_count

    def switch_to_multiindex(self):
        # determine if a certain number of columns is multiindex based on uniqueness of columns (very low, many repeated similar items) and most_common_spacy_tag_ratio (very high, consistent the same type)
        res = self
        columns = self.data.columns
        multiindex_columns = []
        for col in columns:
            if col in self.metadata:
                if (
                    self.metadata[col]["uniqueness_index"] < 0.2
                    and self.metadata[col]["most_common_spacy_tag_ratio"] > 0.8
                ):
                    multiindex_columns.append(col)

        # if the number of columns is multiindex, return the list of columns that are multiindex
        # if the number of columns is not multiindex, return None
        if len(multiindex_columns) > 1:
            df = self.data
            df.set_index(["Store", "Category", "Subcategory"], inplace=True)
            df.sort_index(inplace=True)

            res = MultiIndexTable(df)
            res.metadata = self.metadata
            res.columns = self.columns
            res.rows = self.rows
            res.process_all()
        return res, multiindex_columns

    def process_all(self):
        for col in self.columns:
            uniqueness_index = self.uniqueness_index_col_data(col)
            null_ratio = self.null_ratio_col_data(col)
            spacy_tag = self._nlp_model(col)
            (
                most_common_spacy_tag,
                most_common_spacy_tag_ratio,
                spacy_tag_count,
            ) = self.__process__column__tags__(col)
            if most_common_spacy_tag_ratio > 0.5:
                is_number_col = self.is_number_col(col, most_common_spacy_tag)
            else:
                is_number_col = self.is_number_col(col)
            self.metadata[col] = {
                "uniqueness_index": uniqueness_index,
                "null_ratio": null_ratio,
                "is_number_col": is_number_col,
                "spacy_tag": spacy_tag[0].tag_,
                "most_common_spacy_tag": most_common_spacy_tag,
                "most_common_spacy_tag_ratio": most_common_spacy_tag_ratio,
                "spacy_tag_count": spacy_tag_count,
            }
            if self.VERBOSE:
                print(f"Column: {col}")
                print(f"Uniqueness index: {uniqueness_index}")
                print(f"Null ratio: {null_ratio}")
                print(f"Most common spacy tag: {most_common_spacy_tag}")
                print(f"Most common spacy tag ratio: {most_common_spacy_tag_ratio}")
                print(f"Most common spacy tag count: {spacy_tag_count}")
                print(f"Is number col: {is_number_col}")
                print(f"Spacy tag_: {spacy_tag[0].tag_}")
                print(f"Spacy pos_: {spacy_tag[0].pos_}")

    def is_data_col(self, col_name: str) -> bool:
        # the the most common spacy tags
        if col_name in self.metadata:
            if "most_common_spacy_tag" in self.metadata[col_name]:
                if "most_common_spacy_tag_ratio" in self.metadata[col_name]:
                    if self.metadata[col_name]["most_common_spacy_tag_ratio"] > 0.5:
                        if (
                            self.metadata[col_name]["most_common_spacy_tag"] == "DATE"
                            or self.metadata[col_name]["most_common_spacy_tag"]
                            == "TIME"
                        ):
                            return True
        return False

    def is_number_col(self, col_name: str, most_common_spacy_tag: str = None) -> bool:
        # check if most strings in the column are numbers
        if most_common_spacy_tag is not None:
            return (
                most_common_spacy_tag.lower() == "num"
                or most_common_spacy_tag.lower() == "cd"
                or most_common_spacy_tag.lower() == "cardinal"
                or most_common_spacy_tag.lower() == "quantity"
            )
        col = self.data[col_name]
        counts = 0
        for d in col:
            if isinstance(d, float) or isinstance(d, int):
                counts += 1
                continue
            if isinstance(d, str):
                if d.isdigit():
                    counts += 1
                    continue
                for s in d:
                    if s.isdigit():
                        counts += 1.0 / len(d)
                        continue
        return (counts / len(col)) > 0.5

    def is_long_text_col(self, col_name: str) -> bool:
        col = self.data[col_name]
        counts = 0
        for d in col:
            if isinstance(d, float) or isinstance(d, int):
                continue
            if isinstance(d, str):
                if len(d) > 10:
                    counts += 1
        return (counts / len(col)) > 0.5

    def uniqueness_index_col_data(self, col_name: str) -> float:
        # calculate the number of uniques elements in the column
        col = self.data[col_name]
        return len(col.unique()) / len(col)

    def null_ratio_col_data(self, col_name: str) -> float:
        # calculate the ratio of null elements in the column
        col = self.data[col_name]
        return col.isnull().sum() / len(col)

    def __gen_obj_cols__(self, phrase, linking_predicates, row, object_columns):
        previous_linking_predicate = ""
        for idx, col2 in enumerate(object_columns):
            if idx > 0:
                if idx == len(object_columns) - 1:
                    if previous_linking_predicate == linking_predicates[col2] and (
                        previous_linking_predicate == "is"
                        or previous_linking_predicate == "are"
                        or previous_linking_predicate == "has"
                        or previous_linking_predicate == "have"
                    ):
                        phrase += f" and "
                    else:
                        phrase += " "
                elif previous_linking_predicate == linking_predicates[col2]:
                    phrase += f", "
                elif (
                    previous_linking_predicate == "with"
                    or previous_linking_predicate == "in"
                    or previous_linking_predicate == "on the date of"
                ):
                    phrase += f" "
                elif (
                    previous_linking_predicate == "is"
                    or previous_linking_predicate == "are"
                    or previous_linking_predicate == "has"
                    or previous_linking_predicate == "have"
                ):
                    phrase += f", "
                phrase += f"{linking_predicates[col2]} "
            else:
                phrase += f"{linking_predicates[col2]} "
            if self.__include__colname__in__phrase__(col2, linking_predicates[col2]):
                phrase += f"{row[col2]} {col2}"
            else:
                phrase += f"{row[col2]}"
            previous_linking_predicate = linking_predicates[col2]
        return phrase, previous_linking_predicate

    def generate_phrase(self, row):
        # generate a phrase from the row
        phrase = ""
        # get row in pandas
        row = self.data.iloc[row]
        # get column names
        columns = self.data.columns

        # choose subject_columns from metadata
        subject_columns = []
        for col in columns:
            if (
                self.metadata[col]["uniqueness_index"] > 0.6
                and self.metadata[col]["null_ratio"] < 0.5
                and self.metadata[col]["is_number_col"] == False
                and self.is_data_col(col) == False
            ):
                subject_columns.append(col)

        if len(subject_columns) > 0:
            # choose subject with lowest index in the column list in the original table
            # get subject column index in the original table
            index_list = [columns.get_loc(col) for col in subject_columns]
            # print(index_list)
            subject_column = subject_columns[index_list.index(min(index_list))]
            subject_columns = [subject_column]

        # choose object_columns from metadata
        object_columns = []
        object_plural = dict()
        for col in columns:
            if (
                col not in subject_columns
                and self.metadata[col]["uniqueness_index"] <= 1.0
                and self.metadata[col]["null_ratio"] < 0.5
            ):
                object_columns.append(col)
                if isinstance(row[col], str):
                    object_plural[col] = True if row[col][-1] == "s" else False
                else:
                    object_plural[col] = False

        # choose linking predicate fo each object
        linking_predicates = dict()
        for col in object_columns:
            is_number = False
            is_date = False
            is_long_text = False
            if col in self.metadata:
                is_number = self.metadata[col]["is_number_col"]
                is_date = self.is_data_col(col)
                is_long_text = self.is_long_text_col(col)
            plural = True if col in object_plural and object_plural[col] else False
            linking_predicates[col] = self.__linking_predicate__(
                is_number,
                plural,
                is_date=is_date,
                is_long_text=is_long_text,
                most_common_spacy_tag=self.metadata[col]["most_common_spacy_tag"],
            )

        # generate phrase
        for col in subject_columns:
            phrase += f"{col} {row[col]} "

        phrase, previous_linking_predicate = self.__gen_obj_cols__(
            phrase, linking_predicates, row, object_columns
        )
        phrase += "."
        return phrase, row

    def generate_all_phrases(self):
        phrases = []
        for row in range(len(self.data)):
            phrase, row = self.generate_phrase(row)
            phrases.append(phrase)
        return phrases


class MultiIndexTable(TableMetadata):
    def __init__(self, table):
        super().__init__(table)
        self.multi_index_metadata = dict()

    def process_all(self):
        # process all as single index
        super().process_all()
        # process all as multiindex
        self.process_multindex_metadata()

    def process_multindex_metadata(self):
        # implement functions that add funcionality of analyzing multiple index
        multinames = self.data.index.names
        for name in multinames:
            # count unique values in the index
            unique_values = self.data.index.get_level_values(name).unique()
            # uniqueness score = number of unique values / number of values
            uniqueness_score = len(unique_values) / len(
                self.data.index.get_level_values(name)
            )
            # null ratio = number of null values / number of values
            null_ratio = self.data.index.get_level_values(name).isnull().sum() / len(
                self.data.index.get_level_values(name)
            )

            # add metadata to multi_index_metadata
            self.multi_index_metadata[name] = {
                "uniqueness_score": uniqueness_score,
                "null_ratio": null_ratio,
            }
            self.multi_index_metadata[name]["spacy_obj"] = self._nlp_model(name)[0]
            # spacy tag
            self.multi_index_metadata[name]["spacy_tag"] = self._nlp_model(name)[0].pos_
            # spacy tag for each unique value
            self.multi_index_metadata[name]["unique_values"] = dict()
            for value in unique_values:
                self.multi_index_metadata[name]["unique_values"][
                    value
                ] = self._nlp_model(value)[0].pos_
            # count of spacy tags
            self.multi_index_metadata[name]["spacy_tag_count"] = dict()
            for value in unique_values:
                tag = self.multi_index_metadata[name]["unique_values"][value]
                if tag not in self.multi_index_metadata[name]["spacy_tag_count"]:
                    self.multi_index_metadata[name]["spacy_tag_count"][tag] = 0
                self.multi_index_metadata[name]["spacy_tag_count"][tag] += 1
            # most common spacy tag
            self.multi_index_metadata[name]["most_common_spacy_tag"] = max(
                self.multi_index_metadata[name]["spacy_tag_count"],
                key=self.multi_index_metadata[name]["spacy_tag_count"].get,
            )
            # most common spacy tag ratio
            self.multi_index_metadata[name][
                "most_common_spacy_tag_ratio"
            ] = self.multi_index_metadata[name]["spacy_tag_count"][
                self.multi_index_metadata[name]["most_common_spacy_tag"]
            ] / len(
                unique_values
            )

    def process_row_multi(self, row):
        # get index by row number
        index = self.data.index[row]
        # get index names
        index_names = self.data.index.names

        multisubject = []
        multiobject = []
        object_columns = []
        temp = sorted(
            (
                (
                    self.multi_index_metadata[name]["uniqueness_score"],
                    (idx, name, index[idx]),
                )
                for idx, name in enumerate(index_names)
            ),
            reverse=True,
        )
        for uni, (idx, name, value) in temp:
            metadata = self.multi_index_metadata[name]
            if metadata["most_common_spacy_tag_ratio"] > 0.8:
                multisubject.append((name, value))
                continue

            # if uniqueness score is high and null ratio is low and most common spacy tag is NOUN
            if (
                metadata["null_ratio"] < 0.5
                and metadata["most_common_spacy_tag"] == "NOUN"
            ):
                # add index to subject_columns
                multisubject.append((name, value))
                continue

            # if uniqueness score is high and null ratio is low and most common spacy tag is not NOUN
            elif (
                metadata["uniqueness_score"] > 0.9
                and metadata["null_ratio"] < 0.5
                and metadata["most_common_spacy_tag"] != "NOUN"
            ):
                # add index to object_columns
                multiobject.append((name, value))
                continue

            # if uniqueness score is low or null ratio is high
            else:
                # add index to object_columns
                multiobject.append((name, value))

        # generate a phrase from the row
        phrase = ""
        # get row in pandas
        row = self.data.iloc[row]
        # get column names
        columns = self.data.columns

        # choose subject_columns from metadata
        subject_columns = []
        for col in columns:
            if (
                self.metadata[col]["uniqueness_index"] > 0.9
                and self.metadata[col]["null_ratio"] < 0.5
                and self.metadata[col]["is_number_col"] == False
                and self.metadata[col]["spacy_tag"] == "NOUN"
            ):
                subject_columns.append(col)
        if len(subject_columns) > 0:
            # choose subject with lowest index in the column list in the original table
            # get subject column index in the original table
            index_list = [columns.get_loc(col) for col in subject_columns]
            subject_column = subject_columns[index_list.index(min(index_list))]
            subject_columns = [subject_column]

        # choose object_columns from metadata
        object_plural = dict()
        for col in columns:
            if (
                col not in subject_columns
                and self.metadata[col]["uniqueness_index"] <= 1.0
                and self.metadata[col]["null_ratio"] < 0.5
            ):
                object_columns.append(col)
                if isinstance(row[col], str):
                    object_plural[col] = True if row[col][-1] == "s" else False
                else:
                    object_plural[col] = False

        # choose linking predicate fo each object
        linking_predicates = dict()
        for col in columns:
            is_number = False
            is_date = False
            is_long_text = False
            if col in self.metadata:
                is_number = self.metadata[col]["is_number_col"]
                is_date = (
                    self.metadata[col]["most_common_spacy_tag"] == "DATE"
                    or self.metadata[col]["most_common_spacy_tag"] == "TIME"
                )
                is_long_text = self.is_long_text_col(col)
            plural = True if col in object_plural and object_plural[col] else False
            linking_predicates[col] = self.__linking_predicate__(
                is_number, plural, is_date=is_date, is_long_text=is_long_text
            )

        for idx, micol in enumerate(multisubject):
            phrase += f"{micol[0]} {micol[1]} "
            if idx < len(multisubject) - 1:
                most_common_spacy_tag = self.multi_index_metadata[micol[0]][
                    "most_common_spacy_tag"
                ]
                if most_common_spacy_tag == "DATE" or most_common_spacy_tag == "TIME":
                    phrase += "on the date of "
                elif (
                    most_common_spacy_tag == "GPE"
                    or most_common_spacy_tag == "LOC"
                    or most_common_spacy_tag == "FAC"
                ):
                    phrase += "in "
                elif most_common_spacy_tag == "PERSON":
                    phrase += "of "
                elif most_common_spacy_tag == "ORG":
                    phrase += "with "
                elif most_common_spacy_tag == "EVENT":
                    phrase += "at "
                else:
                    phrase += "of "

        if len(multiobject) > 0:
            phrase += "for "
        for idx, col2 in enumerate(multiobject):
            phrase += f"{col2[1]} "
            if idx < len(multiobject) - 1:
                phrase += "and "

        phrase, previous_linking_predicate = self.__gen_obj_cols__(
            phrase, linking_predicates, row, object_columns
        )
        phrase += "."
        return phrase, row

    def generate_phrase(self, row):
        res, row = self.process_row_multi(row)
        return res, row
