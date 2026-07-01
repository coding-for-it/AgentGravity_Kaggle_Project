import pandas as pd


class FileMCP:

    def read_csv(self, filepath):

        print(f"\n[MCP] Reading file: {filepath}")

        return pd.read_csv(filepath)

    def save_csv(self, df, filepath):

        df.to_csv(
            filepath,
            index=False
        )

        print(f"[MCP] Saved file: {filepath}")

    def dataframe_summary(self, df):

        return {

            "rows": len(df),

            "columns": len(df.columns),

            "column_names": list(df.columns),

            "missing_values":
                int(df.isna().sum().sum()),

            "memory_mb":
                round(
                    df.memory_usage(deep=True).sum()
                    / 1024
                    / 1024,
                    2
                )

        }

    def preview(self, df, rows=5):

        return df.head(rows)