#############################
## 67978 Project Milestone ##
## Visualize data to       ##
## ensure validity         ##
#############################

library(ggplot2)
library(RColorBrewer)
library(grid)

# Functions

# MAIN

# To allow Hebrew
Sys.setlocale("LC_ALL", "Hebrew")
options(encoding ="UTF-8-BOM")


setwd("C:\\Users\\USER\\Desktop\\gil\\PhD\\year_break_3\\Needle_in_data\\Final_project\\Milestone\\")
# read data
il_edu_2019 = read.csv("education_2019.csv", stringsAsFactors = F, row.names = 1, na.strings = c("..", "-"))
il_edu_2019_cor_bagrut_academy = il_edu_2019[,c("????.??????????", 
                                                "????????.??????????.????????????.??????????.????????.????????????.??????????.????.??????.??.2018.19", 
                                                "??????????.??????????.????????.??????????????.????????????.??????????.????????.8.????????.????????.????????????.????.????.??.2019.20",
                                                "??????????.??????????????.??????????.????????.??????.??????????????.??????.??.2018.19")]

il_population_2020 = read.csv("population_2020.csv", stringsAsFactors = F, row.names = 1)
il_population_2020 = il_population_2020[row.names(il_edu_2019),]



### Vis1: education- checking bagrut and academy correlation

il_edu_2019_cor_bagrut_academy = na.omit(il_edu_2019_cor_bagrut_academy)
colnames(il_edu_2019_cor_bagrut_academy) = c("city_name", "bagrut_perc", "academy_perc", "class_size_avg")




# Check for correlations with pearson's r
cor.test(il_edu_2019_cor_bagrut_academy$bagrut_perc, 
         il_edu_2019_cor_bagrut_academy$academy_perc, method="pearson")
cor.test(il_edu_2019_cor_bagrut_academy$bagrut_perc, 
         il_edu_2019_cor_bagrut_academy$class_size_avg, method="pearson")
cor.test(il_edu_2019_cor_bagrut_academy$academy_perc, 
         il_edu_2019_cor_bagrut_academy$class_size_avg, method="pearson")


# Create a text
grob <- grobTree(textGrob("Pearson r = 0.58\n  p-value = 1.7e-15", x=0.8, y=0.5,
                          gp=gpar(col="#7570b3", fontsize=11, fontface="bold")))
# Plot
grob2 <- grobTree(textGrob("????????-????????", x=0.26, y=0.94,
                           gp=gpar(col="black", fontsize=11)))
grob3 <- grobTree(textGrob("?????????????? ????????", x=0.85, y=0.05,
                           gp=gpar(col="black", fontsize=11)))
grob4 <- grobTree(textGrob("??????????????-??????????-????????", x=0.1, y=0.88,
                           gp=gpar(col="black", fontsize=11)))



ggplot(data = il_edu_2019_cor_bagrut_academy, aes(x=academy_perc, color = class_size_avg)) +
        geom_point(aes(y = bagrut_perc), size = 5, show.legend = T)+
        scale_color_gradient(high = "#e31a1c", low = "#ffffb2")+
        geom_smooth(aes(y = bagrut_perc), method="lm", col = "#7570b3", se = F, linetype = "dashed") +
        labs(x = '???????? ?????????????? ???????????? ??????????', y='???????? ???????????? ???????????? ??????????', color = '???????? ???????? ??????????')+theme_bw()+ 
        annotation_custom(grob)+annotation_custom(grob2)+annotation_custom(grob3)+annotation_custom(grob4)
        # annotate(geom="text", x=45, y=25, label="Pearson r = 0.58\np = 1.7e-15", color="black")
# histogram
# geom_histogram(data = STAD_tgf_beta[STAD_tgf_beta$SBS20 == 0,], 
               # aes(y =ifelse(stat(count) > 0, -stat(count)/100, NA)), bins = 110, fill = "#f4cae4", 
               # show.legend = FALSE, size=3)


### Vis2: Population- checking that city size distribution makes sense, and that there are no unrealistic values.

organize_population_number = function(population_number){
        if(grepl( ",", population_number, fixed = TRUE)){
                first = strsplit(population_number, ",")[[1]][1]
                second = strsplit(population_number, ",")[[1]][2]
                return(as.numeric(paste0(first, second)))
        }
        return(as.numeric(population_number))
}

colnames(il_population_2020) = c("city", "overall_population", "male_pop", "female_pop")
# fix numbers
il_population_2020$overall_population = sapply(il_population_2020$overall_population, organize_population_number)
il_population_2020$male_pop = sapply(il_population_2020$male_pop, organize_population_number)
il_population_2020$female_pop = sapply(il_population_2020$female_pop, organize_population_number)


grob_population <- grobTree(textGrob("??????????????", x=0.92, y=0.1,
                           gp=gpar(col="black", fontsize=11)))

grob_population2 <- grobTree(textGrob("???? ????????", x=0.48, y=0.1,
                                     gp=gpar(col="black", fontsize=11)))


ggplot(data=il_population_2020, aes(x = overall_population/1000)) + 
        geom_histogram(aes(y =..density..),
                       breaks=seq(0, 1000, by = 10),
                       col="#2c7bb6",
                       fill="#2c7bb6") +
        labs(title="Distribution of city population in israel", x="Population size (thousands)", y='Population size frequency')+theme_bw()+
        annotation_custom(grob_population)+annotation_custom(grob_population2)


grob_population3 <- grobTree(textGrob("????????", x=0.91, y=0.1,
                                      gp=gpar(col="black", fontsize=11)))
ggplot(data=il_population_2020, aes(x = log(overall_population))) + 
        geom_histogram(aes(y =..density..),
                       # breaks=seq(0, 300, by = 10),
                       col="#2c7bb6",
                       fill="#2c7bb6") +
        labs(title="Distribution of city population in israel (Largest cities removed)", x="log(Population size)", y='Population size frequency')+theme_bw()
        
# annotation_custom(grob_population3)

# ggplot(il_population_2020, aes(fill=condition, y=value, x=specie)) + 
#         geom_bar(position="dodge", stat="identity")
