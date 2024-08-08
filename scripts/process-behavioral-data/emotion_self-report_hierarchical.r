library(tidyverse) 
library(here)

setwd(here())

d <- read.csv('data/general_data/behavioral_data.csv')

cols <- data.frame(
    assessment = c(
        "Negative Affect (Sadness, Fear, Anger)",
        "Negative Affect (Sadness, Fear, Anger)",
        "Negative Affect (Sadness, Fear, Anger)",
        "Negative Affect (Sadness, Fear, Anger)",
        "Negative Affect (Sadness, Fear, Anger)",
        "Negative Affect (Sadness, Fear, Anger)",
        "Psychological Well-being (Positive Affect, Life Satisfaction, Meaning and Purpose)",
        "Psychological Well-being (Positive Affect, Life Satisfaction, Meaning and Purpose)",
        "Psychological Well-being (Positive Affect, Life Satisfaction, Meaning and Purpose)",
        "Social Relationships (Social Support, Companionship, Social Distress, Positive Social Development)",
        "Social Relationships (Social Support, Companionship, Social Distress, Positive Social Development)",
        "Social Relationships (Social Support, Companionship, Social Distress, Positive Social Development)",
        "Social Relationships (Social Support, Companionship, Social Distress, Positive Social Development)",
        "Social Relationships (Social Support, Companionship, Social Distress, Positive Social Development)",
        "Social Relationships (Social Support, Companionship, Social Distress, Positive Social Development)",
        "Stress and Self Efficacy (Perceived Stress, Self-Efficacy)",
        "Stress and Self Efficacy (Perceived Stress, Self-Efficacy)"
    ),
    column_header = c(
        "AngAffect_Unadj",
        "AngHostil_Unadj",
        "AngAggr_Unadj",
        "FearAffect_Unadj",
        "FearSomat_Unadj",
        "Sadness_Unadj",
        "LifeSatisf_Unadj",
        "MeanPurp_Unadj",
        "PosAffect_Unadj",
        "Friendship_Unadj",
        "Loneliness_Unadj",
        "PercHostil_Unadj",
        "PercReject_Unadj",
        "EmotSupp_Unadj",
        "InstruSupp_Unadj",
        "PercStress_Unadj",
        "SelfEff_Unadj"
    )
)

# Format cols
colnames(cols)[2] <- 'item'
d <- d[, c('Subject', cols$item)]
cols$item <- tolower(cols$item)
cols$item <- sapply(cols$item, gsub, pattern = '_unadj', replacement = '')
abbrev <- c('negative_affect', 'well_being', 'relationships', 'stress_efficacy')
cols <- inner_join(cols, data.frame(assessment=unique(cols$assessment), abbrev=abbrev))

colnames(d) <- tolower(colnames(d))
d <- d[complete.cases(d),]
colnames(cols)[colnames(cols) == 'column_header'] <- 'item'
colnames(d) <- sapply(colnames(d), gsub, pattern = '_unadj', replacement = '')

# drop non diagnostic items
relationships <- cols[cols$abbrev=='relationships',]$item
stress_efficacy <- cols[cols$abbrev=='stress_efficacy', ]$item
d <- d[, !colnames(d) %in% c(relationships, stress_efficacy)]

## HIERARCHICAL CLUSTERING

# Build tree
distances <- dist(d[,2:(ncol(d))], method='euclidean')
hc <- hclust(distances, method='complete')

# Iterate over number of clusters
nclusters <- 10
result <- data.frame()
for (k in 1:nclusters) {
    clusters <- cutree(hc, k=k)
    sil <- cluster::silhouette(clusters, dist(d[,2:ncol(d)]))
    sil_width <- mean(data.frame(sil)$sil_width)
    trial <- data.frame(clusters=k, sil_width=sil_width)
    result <- rbind(result, trial)
}

plot(result)
clusters <- cutree(hc, k=2)
summary(factor(clusters))

# Best characterized by three groups but one group is very small

d$cluster <- clusters

d %>% 
    gather(item, response, angaffect:posaffect) %>% 
    inner_join(cols[,c('item', 'abbrev')]) %>% 
    group_by(abbrev, cluster) %>% 
    summarize(response_ = mean(response), se = sd(response) / sqrt(n())) %>% 
    ggplot(aes(x = abbrev, y = response_)) + 
    geom_bar(stat='identity') + 
    geom_errorbar(aes(ymin = response_ - se, ymax = response_ + se), width = .5) + 
    facet_wrap(~cluster) + 
    theme(axis.text.x = element_text(angle = 45, hjust=1))
















