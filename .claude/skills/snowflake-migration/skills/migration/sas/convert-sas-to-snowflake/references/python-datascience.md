# Python Data Science Reference

Translation patterns for SAS statistical/ML procedures to Python.

---

## Snowpark Session Setup

```python
# Cell 1: Setup
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session
import pandas as pd
import numpy as np

session = get_active_session()
TARGET_SCHEMA = "DATABASE.SCHEMA"

def read_table(table_name):
    """Read Snowflake table to pandas DataFrame"""
    return session.table(f"{TARGET_SCHEMA}.{table_name}").to_pandas()

def write_table(df, table_name):
    """Write pandas DataFrame to Snowflake"""
    session.write_pandas(df, table_name, auto_create_table=True, overwrite=True)
```

---

## PROC MEANS → pandas

### Basic Statistics

```sas
/* SAS */
PROC MEANS DATA=mydata N NMISS MEAN STD MIN MAX;
    VAR score1 score2 score3;
RUN;
```

```python
# Python
df = read_table("mydata")
stats = df[['score1', 'score2', 'score3']].agg(['count', 'mean', 'std', 'min', 'max'])
print(stats)
```

### With OUTPUT Statement

```sas
/* SAS */
PROC MEANS DATA=mydata NOPRINT;
    VAR sales;
    BY region;
    OUTPUT OUT=summary_stats MEAN=avg_sales SUM=total_sales N=count;
RUN;
```

```python
# Python
df = read_table("mydata")
summary = df.groupby('region')['sales'].agg(
    avg_sales='mean',
    total_sales='sum',
    count='count'
).reset_index()
write_table(summary, "summary_stats")
```

---

## PROC UNIVARIATE → scipy.stats

```sas
/* SAS */
PROC UNIVARIATE DATA=mydata;
    VAR score;
    HISTOGRAM / NORMAL;
    OUTPUT OUT=univ_stats MEAN=mean STD=std SKEWNESS=skew KURTOSIS=kurt;
RUN;
```

```python
# Python
from scipy import stats

df = read_table("mydata")
score = df['score'].dropna()

univ_stats = {
    'mean': score.mean(),
    'std': score.std(),
    'skew': stats.skew(score),
    'kurtosis': stats.kurtosis(score),
    'median': score.median(),
    'min': score.min(),
    'max': score.max(),
    'n': len(score),
    'nmiss': df['score'].isna().sum()
}

# Normality test
shapiro_stat, shapiro_p = stats.shapiro(score[:5000])  # Shapiro limited to 5000
univ_stats['shapiro_stat'] = shapiro_stat
univ_stats['shapiro_pvalue'] = shapiro_p

print(pd.Series(univ_stats))
write_table(pd.DataFrame([univ_stats]), "univ_stats")
```

---

## PROC CORR → pandas

```sas
/* SAS */
PROC CORR DATA=mydata;
    VAR var1 var2 var3 var4;
RUN;
```

```python
# Python
df = read_table("mydata")
corr_matrix = df[['var1', 'var2', 'var3', 'var4']].corr()
print(corr_matrix)
write_table(corr_matrix.reset_index(), "correlation_matrix")
```

---

## PROC TTEST → scipy.stats

```sas
/* SAS */
PROC TTEST DATA=mydata;
    CLASS group;
    VAR score;
RUN;
```

```python
# Python
from scipy import stats

df = read_table("mydata")
group_a = df[df['group'] == 'A']['score']
group_b = df[df['group'] == 'B']['score']

# Independent t-test
t_stat, p_value = stats.ttest_ind(group_a, group_b)
print(f"t-statistic: {t_stat}, p-value: {p_value}")

# Levene's test for equal variances
levene_stat, levene_p = stats.levene(group_a, group_b)
print(f"Levene's test: stat={levene_stat}, p={levene_p}")
```

---

## PROC REG → statsmodels

```sas
/* SAS */
PROC REG DATA=mydata;
    MODEL y = x1 x2 x3;
    OUTPUT OUT=reg_results P=predicted R=residual;
RUN;
```

```python
# Python
import statsmodels.api as sm

df = read_table("mydata")
X = df[['x1', 'x2', 'x3']]
X = sm.add_constant(X)  # Add intercept
y = df['y']

model = sm.OLS(y, X).fit()
print(model.summary())

# Output predictions and residuals
df['predicted'] = model.predict(X)
df['residual'] = model.resid
write_table(df, "reg_results")
```

---

## PROC LOGISTIC → sklearn

```sas
/* SAS */
PROC LOGISTIC DATA=mydata;
    MODEL target(event='1') = x1 x2 x3;
    OUTPUT OUT=logistic_results P=prob_1;
RUN;
```

```python
# Python
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

df = read_table("mydata")
X = df[['x1', 'x2', 'x3']]
y = df['target']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit model
model = LogisticRegression()
model.fit(X_scaled, y)

# Predictions
df['prob_1'] = model.predict_proba(X_scaled)[:, 1]
df['predicted_class'] = model.predict(X_scaled)

print(f"Coefficients: {dict(zip(['x1','x2','x3'], model.coef_[0]))}")
print(f"Intercept: {model.intercept_[0]}")

write_table(df, "logistic_results")
```

---

## PROC CLUSTER → sklearn

```sas
/* SAS */
PROC CLUSTER DATA=mydata METHOD=WARD;
    VAR x1 x2 x3;
    ID customer_id;
RUN;
```

```python
# Python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

df = read_table("mydata")
X = df[['x1', 'x2', 'x3']]

# Hierarchical clustering (Ward method)
clustering = AgglomerativeClustering(n_clusters=5, linkage='ward')
df['cluster'] = clustering.fit_predict(X)

write_table(df, "clustered_data")
```

---

## PROC FACTOR → sklearn

```sas
/* SAS */
PROC FACTOR DATA=mydata NFACTORS=3 ROTATE=VARIMAX;
    VAR x1 x2 x3 x4 x5;
RUN;
```

```python
# Python
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler

df = read_table("mydata")
X = df[['x1', 'x2', 'x3', 'x4', 'x5']]

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Factor analysis
fa = FactorAnalysis(n_components=3, rotation='varimax')
factors = fa.fit_transform(X_scaled)

# Factor loadings
loadings = pd.DataFrame(
    fa.components_.T,
    columns=['Factor1', 'Factor2', 'Factor3'],
    index=['x1', 'x2', 'x3', 'x4', 'x5']
)
print("Factor Loadings:")
print(loadings)

# Add factor scores to data
df['factor1'] = factors[:, 0]
df['factor2'] = factors[:, 1]
df['factor3'] = factors[:, 2]
write_table(df, "factor_results")
```

---

## DATA _NULL_ (Reporting) → Python print

```sas
/* SAS */
DATA _NULL_;
    SET summary;
    FILE PRINT;
    PUT 'Total Sales: ' total_sales dollar12.2;
    PUT 'Average: ' avg_sales 8.2;
RUN;
```

```python
# Python
df = read_table("summary")
row = df.iloc[0]

print("=" * 40)
print(f"Total Sales: ${row['total_sales']:,.2f}")
print(f"Average: {row['avg_sales']:.2f}")
print("=" * 40)
```

---

## Library Mapping Reference

| SAS Procedure | Python Library | Function/Class |
|---------------|----------------|----------------|
| PROC MEANS | pandas | `.describe()`, `.agg()` |
| PROC UNIVARIATE | scipy.stats | `describe()`, `skew()`, `kurtosis()` |
| PROC CORR | pandas | `.corr()` |
| PROC TTEST | scipy.stats | `ttest_ind()`, `ttest_rel()` |
| PROC ANOVA | scipy.stats | `f_oneway()` |
| PROC REG | statsmodels | `OLS()` |
| PROC GLM | statsmodels | `GLM()` |
| PROC LOGISTIC | sklearn | `LogisticRegression()` |
| PROC CLUSTER | sklearn | `AgglomerativeClustering()` |
| PROC FACTOR | sklearn | `FactorAnalysis()` |
| PROC PRINCOMP | sklearn | `PCA()` |
| PROC DISCRIM | sklearn | `LinearDiscriminantAnalysis()` |
