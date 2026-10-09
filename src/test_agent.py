import json
import pandas as pd

def testing(agent_state, dataset_path, eda_report):
    
    dataset = pd.read_csv(dataset_path)

    python_code = agent_state["python_code"]
    
    namespace = {}
    
    
    try:
        exec(python_code, namespace)
        test_cleaned_data = namespace["clean_dataframe"](dataset, eda_report)
        
        print("Dirty Dataset:\n")
        print("Null Values:")
        print(dataset.isnull().sum())
        print("\n Outliers in dataset:")
        print(dataset.shape)
        print("Cleaned Dataset:\n")
        print("Null Values:")
        print(test_cleaned_data.isnull().sum())
        print("\n Outliers in cleaned dataset:")
        print(test_cleaned_data.shape)
        
        if test_cleaned_data.shape[0] == 0:
            return False, "The cleaned dataset is empty."
        else:
            if test_cleaned_data.shape[0]/dataset.shape[0] < 0.8:
                return False, "The cleaned dataset retains less than 80% of the original data, which may indicate excessive cleaning."
            else:
                if test_cleaned_data.isnull().sum().sum() == dataset.isnull().sum().sum():
                    return False, "The cleaned dataset has the same number of null values as the original dataset, which may indicate that no cleaning was performed."
                else:
                    
                    total_rows = dataset.shape[0]
                    imputable_cols = [col for col in eda_report["nulls"] if 0 < eda_report["nulls"][col] / total_rows < 0.8]
                    failed_cols = [col for col in imputable_cols if test_cleaned_data[col].isnull().sum() > 0]
                    
                    if failed_cols:
                            detalles = {col: test_cleaned_data[col].isnull().sum() for col in failed_cols}
                            return False, f"Cleaning incomplete. Imputable columns still have nulls: {detalles}"
                    else:
                        return True, "Test passed successfully."

    except Exception as e:
        return False, f"Test failed with error: {str(e)}"