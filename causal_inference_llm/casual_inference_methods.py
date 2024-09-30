import numpy as np
import networkx as nx
from dowhy import CausalModel
from dowhy.gcm.falsify import falsify_graph
import matplotlib.pyplot as plt
import causalpy as cp


## Utilities -----------------------------------------------------

import sys
from io import StringIO

def capture_console_output(func, *args, **kwargs):
    # Redirect stdout to a StringIO object
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        # Call the function
        func(*args, **kwargs)
        # Get the printed output as a string
        output = sys.stdout.getvalue()
    finally:
        # Restore the original stdout
        sys.stdout = old_stdout

    return output
## Do-calculus with DoWhy and Refutations
def dowhy_causal_inference(
    data,
    treatment,
    outcome,
    n_graph,
    effect_modifiers,
    target_units,
    method,
    method_params):
    """
    Run a causal analysis using the DoWhy library.
    
    Args:
        data (pandas.DataFrame): The input data.
        treatment (str): The name of the treatment variable.
        outcome (str): The name of the outcome variable.
        n_graph (str): The causal graph (node-link format).
        effect_modifiers (list, optional): The effect modifiers for the causal effect.
        target_units (str, optional): The target units for the causal effect.
        method (str, optional): The method to use for estimating the causal effect.
            - Available methods from DoWhy:
                - backdoor.linear_regression
                - backdoor.distance_matching
                - backdoor.propensity_score_stratification
                - backdoor.propensity_score_matching
                - backdoor.propensity_score_weighting
                - iv.instrumental_variable
                - iv.regression_discontinuity
        method_params (dict, optional): The parameters for the chosen method.
    
    Returns:
        string of:
            tuple: A tuple containing the following:
                - identified_estimand (dict): The identified causal effect.
                - causal_estimate (dict): The estimated causal effect.
                - refutes (list): A list of refutation tests and their results.
                - graph (networkx.DiGraph): The causal graph.
            if None of the above are returned, then the causal effect is unidentifiable.
            if the causal effect is identifiable but not estimable, then the causal_estimate will be None.
            if the causal effect is estimable but the refutation tests fail, then the refutes will contain
            the failures with the error message.
    """
    try:
        # Convert node-link format to Graph
        graph: nx.Graph = nx.node_link_graph(n_graph)
        # Remove link with weight = -1
        for link in n_graph['links']:
            if link['weight'] == -1:
                graph.remove_edge(link['source'], link['target'])
    except Exception as e:
        graph = None
    try:
        model = CausalModel(
            data=data,
            graph=graph,
            treatment=treatment,
            outcome=outcome,
            effect_modifiers=effect_modifiers,
        )
    except Exception as e:
        return "Error while creating the model: " + str(e)
    try:
        ## Identify the causal effect
        #   We say that Treatment causes Outcome if changing Treatment leads to a change
        #   in Outcome keeping everything else constant.
        #   Thus in this step, by using properties of the causal graph,
        #   we identify the causal effect to be estimated
        
        identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
    except Exception as e:
        return f"""
            identified_estimand: Error - {e}\n
            causal_estimand: None\n
            refutes: None\n
            causal_graph: \n{nx.node_link_data(model._graph._graph)}\n
            """
    
    estimate = None
    refutes = []

    try:
        # Estimate the effects and run refutation tests
        # IMPORTANT: method_params depend on the method used!
        
        estimate = model.estimate_effect(
            identified_estimand,
            method_name=method,
            target_units=target_units,
            confidence_intervals=True,
            method_params=method_params,
            test_significance=True,
        )
        
        # Refute the results
        
        # -------------------------------------------
        # Random Common Cause:
        #   Adds randomly drawn covariates to data and re-runs the analysis
        #   to see if the causal estimate changes or not. If our assumption was
        #   originally correct then the causal estimate shouldn't change by much.
        try:
            refute_results1 = model.refute_estimate(identified_estimand, estimate,
                                       method_name="random_common_cause")
            refutes.append({"Method": "random_common_cause", "Results": str(refute_results1)})
            
        except Exception as e:
            refutes.append({"Method": "random_common_cause", "Results": f"Failed: {str(e)}"})
        # -------------------------------------------
        
        # -------------------------------------------
        # Placebo Treatment Refuter:
        #   Randomly assigns any covariate as a treatment and re-runs the analysis.
        #   If our assumptions were correct then this newly found out estimate
        #   should go to 0.
        try:
            refute_results2 = model.refute_estimate(identified_estimand, estimate,
                                       method_name="placebo_treatment_refuter")
            refutes.append({"Method": "placebo_treatment_refuter", "Results": str(refute_results2)})
            
        except Exception as e:
            refutes.append({"Method": "placebo_treatment_refuter", "Results": f"Failed: {str(e)}"})
        # -------------------------------------------
        
        # -------------------------------------------
        # Data Subset Refuter:
        #   Creates subsets of the data (similar to cross-validation) and checks
        #   whether the causal estimates vary across subsets. If our assumptions
        #   were correct there shouldn't be much variation.
        try:
            refute_results3=model.refute_estimate(identified_estimand, estimate,
                                       method_name="data_subset_refuter")
            refutes.append({"Method": "data_subset_refuter", "Results": str(refute_results3)})
            
        except Exception as e:
            refutes.append({"Method": "data_subset_refuter", "Results": f"Failed: {str(e)}"})
        
        # -------------------------------------------
        # Add Unobserved Common Cause:
        #   This refutation does not return a p-value. Instead, it provides a sensitivity test
        #   on how quickly the estimate changes if the identifying assumptions (used in identify_effect)
        #   are not valid. Specifically, it checks sensitivity to violation of the backdoor assumption:
        #   that all common causes are observed.
        try:    
            res_unobserved = model.refute_estimate(identified_estimand, estimate, method_name="add_unobserved_common_cause",
                                           confounders_effect_on_treatment="binary_flip", confounders_effect_on_outcome="linear",
                                           effect_strength_on_treatment=[0.001, 0.005, 0.01, 0.02],
                                           effect_strength_on_outcome=[0.001, 0.005, 0.01,0.02]
                                           )
            res_string = f"""
                {res_unobserved.refutation_type}
                Estimated effect: {res_unobserved.estimated_effect}
                New Effect Range (must not include 0): {res_unobserved.new_effect}
                """
            refutes.append({"Method": "add_unobserved_common_cause", "Results": res_string})
        except Exception as e:
            refutes.append({"Method": "add_unobserved_common_cause", "Results": f"Failed: {str(e)}"})
        # -------------------------------------------
        
    except Exception as e:
        estimate = f"Error: {e}"

    
    return f"""
        identified_estimand: {str(identified_estimand)}\n
        causal_estimand: {str(estimate)}\n
        refutes: {str(refutes)}\n
        causal_graph: \n{nx.node_link_data(model._graph._graph)}\n
        """
        
# Do Why falsify DAG
def dowhy_falsify_dag(graph, data):
    try:
        G = nx.node_link_graph(graph)
        result = falsify_graph(G, data)
        return str(result.summary())
    except Exception as e:
        return f'Error while falsifying: {e}'

## Causal Py Methods
# ANCOVA
def run_causalpy_ancova(
    data,
    outcome,
    pretreatment_variable_name,
    group_variable_name,
) -> cp.pymc_experiments.PrePostNEGD:
    # Prepare the formula
    formula = f"{outcome} ~ 1 + C({group_variable_name}) + {pretreatment_variable_name}"

    # Run ANCOVA
    result = cp.pymc_experiments.PrePostNEGD(
        data,
        formula,
        group_variable_name,
        pretreatment_variable_name,
        model=cp.pymc_models.LinearRegression(),
    )

    return {
        'result': result,
        'summary': capture_console_output(result.summary),
    }

# Synthetic Control
def run_casualpy_syntheticcontrol(
    data,
    actual,
    intercept,
    treatment_time,
    covariates) -> cp.pymc_experiments.SyntheticControl:
    
    # Prepare the formula
    if len(covariates) == 0:
        formula = f"{actual} ~ {intercept}"
    else:
        formula = f"{actual} ~ {intercept} + {' + '.join(covariates)}"
    print(formula)
    result = cp.pymc_experiments.SyntheticControl(
        data,
        treatment_time,
        formula=formula,
        model=cp.pymc_models.WeightedSumFitter(
            sample_kwargs={"target_accept": 0.95}
    ),
    )

    return {
        'result': result,
        'summary': capture_console_output(result.summary),
    }

# Diff in Diff
def run_casualpy_differenceindifferences(
    data,
    outcome,
    recieved_treatment,
    time_variable_name,
    group_variable_name) -> cp.pymc_experiments.DifferenceInDifferences:
    # Prepare the formula
    formula = f"{outcome} ~ 1 + {group_variable_name} * {recieved_treatment}"

    did_result = cp.pymc_experiments.DifferenceInDifferences(
        data,
        formula,
        time_variable_name=time_variable_name,
        group_variable_name=group_variable_name,
        model=cp.pymc_models.LinearRegression()
    )

    return {
        'result': did_result,
        'summary': capture_console_output(did_result.summary),
    }

# Regression Discontinuity
def run_casualpy_regressiondiscontinuity(
    data,
    outcome,
    running_variable_name,
    treatment_variable,
    treatment_threshold,
    bandwidth=None,
    use_splines=False,
    spline_df=6,
    epsilon=0.001
) -> cp.pymc_experiments.RegressionDiscontinuity:

    if bandwidth is None:
        bandwidth = np.inf

    # Prepare the formula
    if use_splines:
        formula = (
            f"{outcome} ~ 1 + bs({running_variable_name}, df={spline_df}) + {treatment_variable}"
        )
    else:
        formula = f"{outcome} ~ 1 + {running_variable_name} + {treatment_variable}"

    rd_result = cp.pymc_experiments.RegressionDiscontinuity(
        data,
        formula,
        running_variable_name=running_variable_name,
        model=cp.pymc_models.LinearRegression(),
        treatment_threshold=treatment_threshold,
        bandwidth=bandwidth,
        epsilon=epsilon,
    )

    return rd_result

# Instrumental Variables Regression
def run_causalpy_iv(
    data,
    outcome,
    treatment,
    instrument,
    sample_kwargs=None) -> cp.pymc_experiments.InstrumentalVariable:

    formula = f"{outcome} ~ 1 + {treatment}"
    instruments_formula = f"{treatment} ~ 1 + {instrument}"

    iv_result = cp.pymc_experiments.InstrumentalVariable(
        instruments_data=data[[treatment, instrument]],
        data=data[[outcome, treatment]],
        instruments_formula=instruments_formula,
        formula=formula,
        model=cp.pymc_models.InstrumentalVariableRegression(sample_kwargs=sample_kwargs),
    )

    return iv_result