import pandas as pd
import matplotlib.pyplot as plt
import statistics as stat

DATA_SET_NAME = "StudentsPerformance.csv"
READING = "reading score"
WRITING = "writing score"
MATH = "math score"
GENDER = "gender"
PLE = "parental level of education"
ETGROUP = "race/ethnicity"
PREPAR = "test preparation course"

# TODO: Use logging to write the main dataset info

def analys(df):
    print_main_data(df)

    plot_score_data(df)

    plot_gender_data(df)

    plot_parental_education(df)

    plot_middle_scores(df)

    plot_group_data(df)

    plot_preparation_data(df)

    plt.show()



def print_main_data(df):
    print("DATASET 5 lines")
    print(df.head())

    print("\nDATASET TYPES")
    print(df.dtypes)

    print(df.shape)

    cols = list(df.columns)
    # print("Columns: {}".format(cols))

    df_na = {col: list(pd.isna(df[col])).count(True) for col in cols}
    print("NA values:\n", df_na)

    nom_cols_data = [{name: df[col].to_list().count(name) for name in df[col].unique()}
                    for col in cols
                    if df[col].dtype == "object"]
    print(nom_cols_data)

    
# 1
def plot_gender_data(df):
    male_df = df.loc[df[GENDER] == "male"]
    m_num = male_df.shape[0]
    female_df = df.loc[df[GENDER] == "female"]
    f_num = female_df.shape[0]

    gender_pie = pd.DataFrame({"": [m_num, f_num]},
                            index=["Males", "Females"])
    gender_pie.plot.pie(y="",
                        colors=["c", "m"],
                        autopct="%.1f",
                        fontsize=10,
                        figsize=(5, 5))

    
# 2
def plot_parental_education(df):
    par_edu_data = {name: df[PLE].to_list().count(name) for name in df[PLE].unique()}
    # par_edu_data = pd.DataFrame.from_dict(par_edu_df)
    
    labels = []
    nums = []

    for edu, num in par_edu_data.items():
        labels.append(edu)
        nums.append(num)

    par_edu_df = pd.DataFrame({"": nums}, index=labels)

    par_edu_df.plot.pie(y="",
                #  colors=["deepskyblue", "mediumspringgreen", "orange", "orchid"],
                 autopct="%.1f",
                 fontsize=10,
                 figsize=(12, 12))

    plt.axis('equal')


#3
def plot_middle_scores(df):
    middle_reading = stat.mean([int(df[READING][i]) for i in df.index])
    middle_math = stat.mean([int(df[MATH][i]) for i in df.index])
    middle_writing = stat.mean([int(df[WRITING][i]) for i in df.index])

    middle_scores = [middle_reading, middle_math, middle_writing]
    subjects = ["Reading", "Math", "Writing"]

    middles_df = pd.DataFrame({"subject": subjects, "middle score": middle_scores})
    middles_df.plot.barh(x="subject", y="middle score", figsize=(12, 5))


#4
def plot_group_data(df):
    col = ETGROUP
    groups_data = {name: df[col].to_list().count(name) for name in df[col].unique()}
    groups_list = []
    nums = []

    for group, num in groups_data.items():
        groups_list.append(group)
        nums.append(num)

    group_df = pd.DataFrame({"": nums}, index=groups_list)

    group_df.plot.pie(y="",
                #  colors=["deepskyblue", "mediumspringgreen", "orange", "orchid"],
                 autopct="%.1f",
                 fontsize=10,
                 figsize=(12, 12))


#5, 6
def plot_preparation_data(df):
    col = PREPAR
    preparation_data = {name: df[col].to_list().count(name) for name in df[col].unique()}

    preparations = []
    nums = []
    
    for prep, num in preparation_data.items():
        preparations.append(prep)
        nums.append(num)


    prep_df = pd.DataFrame({"": nums}, index=preparations)

    prep_df.plot.pie(y="",
                #  colors=["deepskyblue", "mediumspringgreen", "orange", "orchid"],
                 autopct="%.1f",
                 fontsize=10,
                 figsize=(12, 12))


    for subject in [READING, WRITING, MATH]:
        prepar_df = df.query(f"`{PREPAR}` == 'completed'")[subject]

        prepar_score_data = {score: (prepar_df.to_list().count(score)/len(df.loc[df[PREPAR] == "completed"])) * 100 
                                    for score in set(prepar_df)}
        # print(prepar_score_data)
        prepar_score_df = pd.DataFrame.from_dict(data=prepar_score_data, orient="index", columns=["Prepared"])

        not_prepar_df = df.query(f"`{PREPAR}` == 'none'")[subject]


        not_prepar_score_data = {score: (not_prepar_df.to_list().count(score)/len(df.loc[df[PREPAR] == "none"])) * 100 
                                        for score in set(not_prepar_df)}
        not_prepar_score_df = pd.DataFrame.from_dict(data=not_prepar_score_data, orient="index", columns=["Not prepared"])

        all_pf = prepar_score_df.merge(not_prepar_score_df, left_index=True, right_index=True)
        all_pf.plot(title=subject)



def plot_score_data(df):
    reading_score_stat = {"min": df[READING].min(), 
            "max": df[READING].max(), 
            "mean": df[READING].mean(),
            "median": df[READING].median(),
            "mode": df[READING].mode().to_list(),
            "var": round(df[READING].var(ddof=0), 2),
            "std": round(df[READING].std(ddof=0), 2),
            "range": df[READING].max() - df[READING].min(),
            "interquartile_range": df[READING].quantile(0.75) - df[READING].quantile(0.25),
            "skew": df[READING].skew()
            }
    print(reading_score_stat)

    middle_score_list = [(int(df[READING][i]) + int(df[MATH][i]) + int(df[WRITING][i]))//3 for i in df.index ]
    middle_score_data = {score: middle_score_list.count(score) for score in set(middle_score_list)}

    reading_score_data = {score: df[READING].to_list().count(score) for score in set(df[READING])}
    writing_score_data = {score: df[WRITING].to_list().count(score) for score in set(df[WRITING])}
    math_score_data = {score: df[MATH].to_list().count(score) for score in set(df[MATH])}


    reading_score_df = pd.DataFrame.from_dict(data=reading_score_data, orient="index", columns=["Reading Score"])
    writing_score_df = pd.DataFrame.from_dict(data=writing_score_data, orient="index", columns=["Writing Score"])
    math_score_df = pd.DataFrame.from_dict(data=math_score_data, orient="index", columns=["Math Score"])


    middle_score_df = pd.DataFrame.from_dict(data=middle_score_data, orient="index", columns=["Middle Score"])

    # score_all = middle_score_df.merge(reading_score_df, left_index=True, right_index=True)
    # score_all = score_all.merge(writing_score_df, left_index=True, right_index=True)
    score_all = reading_score_df.merge(writing_score_df, left_index=True, right_index=True)
    score_all = score_all.merge(math_score_df, left_index=True, right_index=True)
    score_all.plot()

    score_reading = middle_score_df.merge(reading_score_df, left_index=True, right_index=True)
    score_writing = middle_score_df.merge(writing_score_df, left_index=True, right_index=True)
    score_math = middle_score_df.merge(math_score_df, left_index=True, right_index=True)

    score_math.plot()
    score_writing.plot()
    score_reading.plot()


if __name__ == "__main__":
    df = pd.read_csv(DATA_SET_NAME)
    analys(df)