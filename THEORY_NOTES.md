# Theory Notes — Derivable Judgement

## 1. Inferential statistics
Inferential statistics uses sample data to estimate population characteristics or test claims about a population. It helps make evidence-based conclusions while accounting for uncertainty.

## 2. Hypothesis testing and components
Hypothesis testing evaluates a claim using sample data. Its components include the null hypothesis (H₀), alternative hypothesis (H₁), significance level (α), test statistic, p-value or critical value, and a decision.

## 3. Confidence interval and critical value
A confidence interval is a range of plausible values for a population parameter, calculated from sample data. A critical value is a cutoff from a probability distribution used to define a rejection region at a chosen significance level.

## 4. P-value
The p-value is the probability, assuming the null hypothesis is true, of observing a result at least as extreme as the one obtained. A small p-value indicates evidence against H₀; it is not the probability that H₀ is true.

## 5. Type I and Type II errors
A Type I error means rejecting a true null hypothesis (false positive). A Type II error means failing to reject a false null hypothesis (false negative).

## 6. z-test, t-test, chi-square test, and ANOVA
- **z-test:** commonly tests a mean or proportion when the relevant standard error is known or a suitable large-sample approximation applies.
- **t-test:** compares means, often when population variance is unknown; Welch's t-test does not assume equal group variances.
- **Chi-square test:** tests whether categorical variables are associated, using observed and expected counts.
- **ANOVA:** tests whether three or more groups have equal means; a significant result indicates at least one mean differs.

## 7. Covariance
Covariance describes how two numerical variables vary together. Positive covariance means they tend to move in the same direction; negative covariance means they tend to move in opposite directions. Its magnitude depends on the variables' units.

## 8. Correlation
Correlation measures the strength and direction of a relationship between variables. Pearson's correlation coefficient ranges from -1 to +1 and measures linear association; correlation alone does not prove causation.

## Decision rule used in this project
At α = 0.05, reject H₀ when p < 0.05; otherwise, fail to reject H₀. “Fail to reject” does not prove H₀ is true.
