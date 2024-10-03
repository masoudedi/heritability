library(ggplot2)
library(dplyr)


file<-'/Users/edi/Desktop/comparision/all.chr.dose_0.3_retained.txt'
file<-'/Users/edi/Desktop/comparision/all.chr.dose_0.3_excluded.txt'
output<-'/Users/edi/Desktop/comparision/'
prefix <- 'imputation_lte_3'
lable <- ' (r2 <= 0.3)'

db = read.csv(file, sep = '\t', col.names = c("rs", "af", "maf", "imputed"))


#create a new category:
summm <- db %>%
  mutate(category = ifelse(maf < 0.01, 'rare', 'common')) %>%
  group_by(category) %>%
  summarize(
    mean = mean(maf, na.rm = TRUE),
    se = sd(maf, na.rm = TRUE) / sqrt(n()),
    count = n(),
    .groups = 'drop'  
  )
ggplot(summm, aes(x = category, y = count, fill = category)) +  
  geom_bar(stat = "identity", alpha = 0.6, color = 'black') + 
  labs(title = paste("Variant Counts by Category", lable),
       x = "Category",
       y = "MVariant Count") +
  scale_fill_manual(values = c("rare" = "skyblue", "common" = "orange")) +  
  theme_minimal()
ggsave(paste(output, prefix, '_count.png'))

ggplot(summm, aes(x = category, y = mean, fill = category)) +  
  geom_bar(stat = "identity", alpha = 0.6, color = 'black') + 
  labs(title = paste("Mean MAF Values by Category", lable),
       x = "Category",
       y = "Mean Minor Allele Frequency (MAF)") +
  scale_fill_manual(values = c("rare" = "skyblue", "common" = "orange")) +  
  theme_minimal()
ggsave(paste(output, prefix, '_mean.png'))

# Histogram
ggplot(db, aes(x = maf)) +
geom_histogram(aes(y = ..density..), bins = 30, fill = "lightblue", color = "black") +
  labs(title = paste("Histogram of MAF", lable),
       x = "Minor Allele Frequency (MAF)",
       y = "Density") +
  scale_x_continuous(breaks = seq(0, 1, by = 0.1)) + 
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
ggsave(paste(output, prefix, '_histogram.png'))

#add category

rare <- db %>%
  filter(maf < 0.01)
common <- db %>%
  filter(maf >= 0.01)

ggplot(rare, aes(x = factor(1), y = maf)) + 
  geom_boxplot(width = 0.2, color = "gray", fill = "skyblue") +  # Custom colors
  labs(title = paste("Distribution of MAF (Rare Category)", lable),
       x = paste("Median value is", median(rare$maf, na.rm = TRUE)),
       y = "MAF") +
  theme_minimal() +
  theme(axis.text.x = element_blank(),
        axis.ticks.x = element_blank())
ggsave(paste(output, prefix, '_rare_box.png'))

ggplot(common, aes(x = factor(1), y = maf)) + 
  geom_boxplot(width = 0.2, color = "gray", fill = "skyblue") +  # Custom colors
  labs(title = paste("Distribution of MAF (Common Category)", lable),
       x = paste("Median value is", median(common$maf, na.rm = TRUE)),
       y = "MAF") +
  theme_minimal() +
  theme(axis.text.x = element_blank(),
        axis.ticks.x = element_blank())
ggsave(paste(output, prefix, '_common_box.png'))
