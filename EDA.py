import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Load Data
filePath = r"C:\Users\sdgz0\Desktop\Data Analyst Portfolio\Stack Overflow Survey\survey_results_public.csv"
df = pd.read_csv(filePath)

# Summary of the dataset
print("Dataset shape:", df.shape)

### Handle Missing Data
# Summary of missing data for key columns
key_columns = ['CompTotal', 'RemoteWork', 'YearsCodePro', 'LearnCode', 'Employment', 'EdLevel', 'LanguageHaveWorkedWith', 'DatabaseHaveWorkedWith', 'PlatformHaveWorkedWith']
missing_summary = df[key_columns].isnull().sum()
print("Missing data summary:\n", missing_summary)

#############################################
# Question 1: How much does remote working matter to employees?
#############################################

# Analyze RemoteWork column
def analyze_remote_work():
    remote_work_counts = df['RemoteWork'].value_counts(normalize=True) * 100
    print("Remote Work Preferences:\n", remote_work_counts)

    # Improved visualization
    remote_work_counts.plot(kind='bar', figsize=(8, 6), color=['#4CAF50', '#2196F3', '#FF9800'], title="Employee Preferences for Remote Work")
    plt.ylabel("Percentage")
    plt.xlabel("Work Arrangement")
    plt.xticks(rotation=0)
    # Add percentages above bars
    for i, v in enumerate(remote_work_counts):
        plt.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=10)
    plt.tight_layout()
    plt.savefig('Remote_Work_Preferences.png')
    plt.show()

analyze_remote_work()

#############################################
# Question 2: How does coding experience affect the level of pay?
#############################################

def analyze_coding_experience_vs_pay():
    # Clean YearsCodePro
    def clean_yearscodepro(value):
        if pd.isna(value):
            return None
        if value == "Less than 1 year":
            return 0
        elif value == "More than 50 years":
            return 51
        else:
            return int(value)

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_yearscodepro)

    # Remove outliers in CompTotal
    df_clean = df.dropna(subset=['YearsCodePro', 'CompTotal'])
    Q1 = df_clean['CompTotal'].quantile(0.25)
    Q3 = df_clean['CompTotal'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_clean = df_clean[(df_clean['CompTotal'] >= lower_bound) & (df_clean['CompTotal'] <= upper_bound)]

    # Group by YearsCodePro
    bins = [0, 2, 5, 10, 20, 30, 50, 60]
    labels = ['0-2', '3-5', '6-10', '11-20', '21-30', '31-50', '51+']
    df_clean['YearsCodeProGroup'] = pd.cut(df_clean['YearsCodePro'], bins=bins, labels=labels, right=False)

    experience_pay = df_clean.groupby('YearsCodeProGroup')['CompTotal'].median()
    group_counts = df_clean['YearsCodeProGroup'].value_counts(normalize=True) * 100

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(experience_pay.index, experience_pay.values, marker='o', linestyle='-', color='#FF5733', label="Median Compensation")

    for i, (group, value) in enumerate(experience_pay.items()):
        percentage = group_counts[group]
        ax.text(i, value + 2000, f'{percentage:.1f}%', ha='center', va='bottom', fontsize=10)

    ax.set_xticks(range(len(experience_pay.index)))
    ax.set_xticklabels(experience_pay.index)
    ax.set_title("Compensation vs. Years of Coding Experience")
    ax.set_xlabel("Years of Experience")
    ax.set_ylabel("Median Compensation")
    plt.grid()
    plt.tight_layout()
    plt.savefig('Compensation_vs_Years_of_Experience.png')
    plt.show()
    

analyze_coding_experience_vs_pay()

#############################################
# Question 3: What is the most popular method of learning code?
#############################################

def analyze_learning_methods():
    learn_code_methods = df['LearnCode'].dropna().str.split(';').explode()
    learn_code_counts = learn_code_methods.value_counts()

    learn_code_online_methods = df['LearnCodeOnline'].dropna().str.split(';').explode()
    learn_code_online_counts = learn_code_online_methods.value_counts()

    # Improved visualization for learning methods
    learn_code_counts.head(10).plot(kind='barh', figsize=(10, 6), color='#6A5ACD', title="Top 10 Methods of Learning to Code")
    plt.xlabel("Number of Responses")
    plt.ylabel("Learning Method")
    plt.tight_layout()
    plt.show()

    learn_code_online_counts.head(10).plot(kind='barh', figsize=(10, 6), color='#4682B4', title="Top 10 Online Methods of Learning to Code")
    plt.xlabel("Number of Responses")
    plt.ylabel("Online Learning Method")
    plt.tight_layout()
    plt.savefig('Top_10_Learning_Methods.png')
    plt.show()

analyze_learning_methods()

#############################################
# Question 4: Are you more likely to get a job as a developer if you have a master's degree?
#############################################


def analyze_education_and_employment():
    # Match the exact roles
    developer_roles = ["Employed, full-time", "Independent contractor, freelancer, or self-employed"]
    developer_data = df[df['Employment'].isin(developer_roles)]

    # Use raw counts
    ed_level_developers = developer_data['EdLevel'].value_counts()
    print("Education Levels of Developers:\n", ed_level_developers)

    # Filter for exact relevant levels
    relevant_levels = [
        "Bachelor’s degree (B.A., B.S., B.Eng., etc.)",
        "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)",
        "Professional degree (JD, MD, Ph.D, Ed.D, etc.)"
    ]
    ed_level_filtered = ed_level_developers[ed_level_developers.index.isin(relevant_levels)]

    # Plot if data is available
    if not ed_level_filtered.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        ed_level_filtered.plot(kind='bar', ax=ax, color='#FFA07A', title="Filtered Education Levels of Developers")
        ax.set_ylabel("Number of Developers")
        ax.set_xlabel("Education Level")
        ax.set_xticklabels(ed_level_filtered.index, rotation=45, ha='right')
        for i, value in enumerate(ed_level_filtered):
            ax.text(i, value + 200, str(value), ha='center', va='bottom', fontsize=10)
        plt.tight_layout()
        plt.savefig('Education_and_employment.png')
        plt.show()
    else:
        print("No data available for the filtered education levels.")



analyze_education_and_employment()


#############################################
# Question 5: What are the most in-demand tech skills?
#############################################

def analyze_in_demand_skills():
    languages = df['LanguageHaveWorkedWith'].dropna().str.split(';').explode()
    databases = df['DatabaseHaveWorkedWith'].dropna().str.split(';').explode()
    platforms = df['PlatformHaveWorkedWith'].dropna().str.split(';').explode()

    tech_skills = pd.concat([languages, databases, platforms])
    tech_skills_counts = tech_skills.value_counts()

    top_tech_skills = tech_skills_counts.head(15)
    # Improved visualization for tech skills
    top_tech_skills.plot(kind='barh', figsize=(10, 6), color='#FF6347', title="Top 15 In-Demand Tech Skills")
    plt.xlabel("Frequency")
    plt.ylabel("Tech Skills")
    plt.tight_layout()
    plt.savefig('Top_15_In_Demand_Tech_Skills.png')
    plt.show()

analyze_in_demand_skills()

#############################################
# End of Script
#############################################

