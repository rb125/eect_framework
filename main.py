import os
import json
from dotenv import load_dotenv
from src.models_config import SUBJECT_MODELS_CONFIG
from src.agent import create_agent
from src.evaluation import EECTEvaluator, calculate_eect_metrics

def main():
    """
    Initializes agents for all subject models and runs a sample EECT experiment for each.
    """
    # Load environment variables from a .env file if it exists
    load_dotenv()

    print("--- EECT Framework Initializing ---")

    # 1. Load the dilemmas
    with open("dilemmas.json", "r") as f:
        dilemmas = json.load(f)

    # Define compression levels
    compression_levels = ["c1.0", "c0.75", "c0.5", "c0.25", "c0.0"]

    # 2. Iterate through all subject models
    for model_config in SUBJECT_MODELS_CONFIG:
        model_name = model_config.get("model_name")
        all_model_results = [] # To store results for this model across all dilemmas and compression levels

        print(f"\n--- Running Evaluation for Model: {model_name} ---")

        print(f"\nAttempting to create agent for: {model_name}")
        try:
            agent = create_agent(model_config)
            print(f"Successfully created agent for '{agent.model_name}'")
        except (ValueError, ImportError) as e:
            print(f"Error creating agent for {model_name}: {e}")
            print("Please ensure your environment variables are set correctly and required packages are installed.")
            continue
        
        # 3. Iterate through all dilemmas and compression levels
        for dilemma in dilemmas:
            print(f"\n  -- Evaluating Dilemma: {dilemma['id']} --")
            dilemma_level_results = [] # To store dialogue results for this dilemma across all compression levels
            for comp_level in compression_levels:
                print(f"    -- Compression Level: {comp_level} --")
                evaluator = EECTEvaluator(agent)
                dialogue_results = evaluator.run_socratic_dialogue(dilemma, comp_level)
                dilemma_level_results.append({
                    "compression_level": comp_level,
                    "dialogue_results": dialogue_results
                })

            # 4. Calculate EECT metrics for this dilemma and append to overall model results
            eect_metrics_for_dilemma = calculate_eect_metrics(dilemma_level_results)
            eect_metrics_for_dilemma["dilemma_id"] = dilemma["id"]
            all_model_results.append(eect_metrics_for_dilemma)
        
        # 4. Save the results to a file
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)
        output_path = os.path.join(results_dir, f"{model_name}_eect_results.json")
        with open(output_path, "w") as f:
            json.dump(all_model_results, f, indent=2)
        print(f"\nResults for {model_name} saved to {output_path}")

if __name__ == "__main__":
    main()

