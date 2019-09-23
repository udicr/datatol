# !diagnostics off
# Title     : "PreProcess"
# Objective : Preprocessing TOL DATA
# Created by: user
# Created on: 20.08.19

library(readxl)
library(dplyr)
library(readr)

args = commandArgs(trailingOnly=TRUE)

if (length(args)==0){
    stop("Argument (PBN_No).n required",call.=FALSE)
}
pbn <- args[1]
print("Doing Preprocess for PBN: ")
print(pbn)

a <- pbn
srfile <- paste0("data/sr_",a,".xls")
frfile <- paste0("data/fr_",a,".xls")
outfile <- paste0("pb",a,".Rda")

df_vs <- read_excel("data/selectedVideos_181219.xlsx")
df_vs$Name_f <- as.factor(df_vs$Name)
df_01_15 <- read.csv("data/daten_01_TOL4_15.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_04_4 <- read.csv("data/daten_04_tol2_4.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_06_4 <- read.csv("data/daten_06_tol1_4.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_06_11 <- read.csv("data/daten_06_tol1_11.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_07_7 <- read.csv("data/daten_07_tol3_7.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_07_8 <- read.csv("data/daten_07_tol3_8.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_07_15 <- read.csv("data/daten_07_tol3_15.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_09_3 <- read.csv("data/daten_09_tol2_3.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_12_2 <- read.csv("data/daten_12_tol1_2.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_12_5 <- read.csv("data/daten_12_tol1_5.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_13_1 <- read.csv("data/daten_07_tol3_15.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_14_6 <- read.csv("data/daten_14_tol2_6.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_15_11 <- read.csv("data/daten_15_tol3_11.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_16_13 <- read.csv("data/daten_16_tol2_13.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_16_14 <- read.csv("data/daten_16_tol2_14.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_17_7 <- read.csv("data/daten_17_tol1_7.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_18_2 <- read.csv("data/daten_18_tol1_2.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_19_2 <- read.csv("data/daten_19_tol3_2.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_19_5 <- read.csv("data/daten_19_tol3_5.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_20_8 <- read.csv("data/daten_20_tol2_8.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_21_11 <- read.csv("data/daten_21_tol3_11.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_21_12 <- read.csv("data/daten_21_tol3_12.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_22_8 <- read.csv("data/daten_22_tol2_8.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_23_10 <- read.csv("data/daten_23_tol1_10.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_26_7 <- read.csv("data/daten_26_tol2_7.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_26_8 <- read.csv("data/daten_26_tol2_8.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_26_12 <- read.csv("data/daten_26_tol2_12.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_27_9 <- read.csv("data/daten_27_tol2_9.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_27_15 <- read.csv("data/daten_27_tol2_15.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_28_6 <- read.csv("data/daten_28_tol3_6.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_29_6 <- read.csv("data/daten_29_tol1_6.txt", header = FALSE, col.names = c("x_coord","y_coord"))
df_31_7 <- read.csv("data/daten_31_tol3_7.txt", header = FALSE, col.names = c("x_coord","y_coord"))

f_num <- function(df) {
  df$frames <- c(1:length(df$x_coord))
  return(df)
}
Spot1 <- f_num(df_20_8)
Spot2 <- f_num(df_19_5)
Spot3 <- f_num(df_28_6)
Spot4 <- f_num(df_27_15)
Spot5 <- f_num(df_27_9)
Spot6 <- f_num(df_29_6)
Spot7 <- f_num(df_26_12)
Spot8 <- f_num(df_14_6)
GL1 <- f_num(df_31_7)
GL2 <- f_num(df_22_8)
GL3 <- f_num(df_17_7)
GL4 <- f_num(df_19_2)
GL5 <- f_num(df_26_7)
GL6 <- f_num(df_06_11)
GL7 <- f_num(df_06_4)
GL8 <- f_num(df_26_8)
BGL1 <- f_num(df_07_8)
BGL2 <- f_num(df_15_11)
BGL3 <- f_num(df_07_15)
BGL4 <- f_num(df_09_3)
BGL5 <- f_num(df_16_13)
BGL6 <- f_num(df_16_14)
BGL7 <- f_num(df_04_4)
BGL8 <- f_num(df_18_2)
Control1 <- f_num(df_21_12)
Control2 <- f_num(df_21_11)
Control3 <- f_num(df_07_7)
Control4 <- f_num(df_01_15)
Control5 <- f_num(df_13_1)
Control6 <- f_num(df_12_5)
Control7 <- f_num(df_12_2)
Control8 <- f_num(df_23_10)

f_cut <- function(x,y){
  sub = df_vs[df_vs$Name == y, ]
  first = sub$first
  last = sub$last
  df = subset(x, frames >= first & frames <= last)
}
Spot1 <- f_cut(Spot1, "Spot1")
Spot2 <- f_cut(Spot2, "Spot2")
Spot3 <- f_cut(Spot3, "Spot3")
Spot4 <- f_cut(Spot4, "Spot4")
Spot5 <- f_cut(Spot5, "Spot5")
Spot6 <- f_cut(Spot6, "Spot6")
Spot7 <- f_cut(Spot7, "Spot7")
Spot8 <- f_cut(Spot8, "Spot8")

GL1 <- f_cut(GL1, "GL1")
GL2 <- f_cut(GL2, "GL2")
GL3 <- f_cut(GL3, "GL3")
GL4 <- f_cut(GL4, "GL4")
GL5 <- f_cut(GL5, "GL5")
GL6 <- f_cut(GL6, "GL6")
GL7 <- f_cut(GL7, "GL7")
GL8 <- f_cut(GL8, "GL8")

BGL1 <- f_cut(BGL1, "BGL1")
BGL2 <- f_cut(BGL2, "BGL2")
BGL3 <- f_cut(BGL3, "BGL3")
BGL4 <- f_cut(BGL4, "BGL4")
BGL5 <- f_cut(BGL5, "BGL5")
BGL6 <- f_cut(BGL6, "BGL6")
BGL7 <- f_cut(BGL7, "BGL7")
BGL8 <- f_cut(BGL8, "BGL8")

Control1 <- f_cut(Control1, "Control1")
Control2 <- f_cut(Control2, "Control2")
Control3 <- f_cut(Control3, "Control3")
Control4 <- f_cut(Control4, "Control4")
Control5 <- f_cut(Control5, "Control5")
Control6 <- f_cut(Control6, "Control6")
Control7 <- f_cut(Control7, "Control7")
Control8 <- f_cut(Control8, "Control8")

df_pb <- read_delim(srfile,"\t", escape_double = FALSE, locale =
                       locale(decimal_mark = ".", grouping_mark = "'"), trim_ws = TRUE)

f_num_2 <- function(df, video) {
  df <- df[rep(1:nrow(df),each=2),] 
  df$frames2 <- c(1:length(df$x_coord))
  df$video <- video
  return(df)
}

Spot1 <- f_num_2(Spot1, "Spot1")
Spot2 <- f_num_2(Spot2, "Spot2")
Spot3 <- f_num_2(Spot3, "Spot3")
Spot4 <- f_num_2(Spot4, "Spot4")
Spot5 <- f_num_2(Spot5, "Spot5")
Spot6 <- f_num_2(Spot6, "Spot6")
Spot7 <- f_num_2(Spot7, "Spot7")
Spot8 <- f_num_2(Spot8, "Spot8")

GL1 <- f_num_2(GL1, "GL1")
GL2 <- f_num_2(GL2, "GL2")
GL3 <- f_num_2(GL3, "GL3")
GL4 <- f_num_2(GL4, "GL4")
GL5 <- f_num_2(GL5, "GL5")
GL6 <- f_num_2(GL6, "GL6")
GL7 <- f_num_2(GL7, "GL7")
GL8 <- f_num_2(GL8, "GL8")

BGL1 <- f_num_2(BGL1, "BGL1")
BGL2 <- f_num_2(BGL2, "BGL2")
BGL3 <- f_num_2(BGL3, "BGL3")
BGL4 <- f_num_2(BGL4, "BGL4")
BGL5 <- f_num_2(BGL5, "BGL5")
BGL6 <- f_num_2(BGL6, "BGL6")
BGL7 <- f_num_2(BGL7, "BGL7")
BGL8 <- f_num_2(BGL8, "BGL8")

Control1 <- f_num_2(Control1, "Control1")
Control2 <- f_num_2(Control2, "Control2")
Control3 <- f_num_2(Control3, "Control3")
Control4 <- f_num_2(Control4, "Control4")
Control5 <- f_num_2(Control5, "Control5")
Control6 <- f_num_2(Control6, "Control6")
Control7 <- f_num_2(Control7, "Control7")
Control8 <- f_num_2(Control8, "Control8")

df_vidco <- rbind(Spot1, Spot2, Spot3, Spot4, Spot5, 
                  Spot6, Spot7, Spot8, GL1, GL2, GL3, GL4, GL5, GL6, GL7, GL8, BGL1, BGL2, BGL3, BGL4, BGL5, BGL6, BGL7, BGL8,  Control1, Control2, Control3, Control4, Control5, Control6, Control7, Control8)

f_frame <- function(df){
  df$SAMPLE_MESSAGE[df$SAMPLE_MESSAGE == "."] <- NA
  FNO <- 0
  
  for (t in 1:32) {
    sub_data <- subset(df, TRIAL_INDEX == t)
    
    for (ip in 1:2) {
      sub2_data <- subset(sub_data, IP_INDEX == ip)
      x <- 0
      condition <- !is.na(sub2_data$SAMPLE_MESSAGE)
      frameNo <- character(nrow(sub2_data))
      for (i in 1:nrow(sub2_data)[condition]) {
        if (condition[i]) {
          frameNo[i] <- x+1
          x <- x+1
        } 
        else {
          frameNo[i] <- x
        }      
      }
      FNO <- append(FNO, frameNo)
    }
  } 
  df$frame <- FNO[2:length(FNO)]
  return(df)
}

f_frame_slow <- function(df){
  df$SAMPLE_MESSAGE[df$SAMPLE_MESSAGE == "."] <- NA
  FNO <- 0
  
  for (t in 1:32) {
    sub_data <- subset(df, TRIAL_INDEX == t)
    x <- 0
    condition <- !is.na(sub_data$SAMPLE_MESSAGE)
    frameNo <- character(nrow(sub_data))
    for (i in 1:nrow(sub_data)[condition]) {
      if (condition[i]) {
        frameNo[i] <- x+1
        x <- x+1
      } 
      else {
        frameNo[i] <- x
      } 
    }     
    FNO <- append(FNO, frameNo)
  } 
  df$frame <- FNO[2:length(FNO)]
  return(df)
}
pbnno <- as.numeric(pbn)
if ((pbnno %% 2) == 0){
    df_pb <- f_frame_slow(df_pb)
    print("SLOW VISUAL")
}
if ((pbnno %% 2) == 1){
    df_pb <- f_frame(df_pb)
    print("FAST VISUAL")
}



f_video <- function(df) {
  df %>% mutate(video = case_when(grepl("20_tol2_8", df$video_file) ~ "Spot1", 
                                  grepl("19_tol3_5", df$video_file) ~ "Spot2", 
                                  grepl("28_tol3_6", df$video_file) ~ "Spot3",
                                  grepl("27_tol2_15", df$video_file) ~ "Spot4",
                                  grepl("27_tol2_9", df$video_file) ~ "Spot5",
                                  grepl("29_tol1_6", df$video_file) ~ "Spot6",
                                  grepl("26_tol2_12", df$video_file) ~ "Spot7",
                                  grepl("14_tol2_6", df$video_file) ~ "Spot8",
                                  grepl("31_tol3_7", df$video_file) ~ "GL1", 
                                  grepl("22_tol2_8", df$video_file) ~ "GL2",
                                  grepl("17_tol1_7", df$video_file) ~ "GL3",
                                  grepl("19_tol3_2", df$video_file) ~ "GL4",
                                  grepl("26_tol2_7", df$video_file) ~ "GL5",
                                  grepl("06_tol1_11", df$video_file) ~ "GL6",
                                  grepl("06_tol1_4", df$video_file) ~ "GL7",
                                  grepl("26_tol2_8", df$video_file) ~ "GL8",
                                  grepl("07_tol3_8", df$video_file) ~ "BGL1",
                                  grepl("15_tol3_11", df$video_file) ~ "BGL2",
                                  grepl("07_tol3_15", df$video_file) ~ "BGL3",
                                  grepl("09_tol2_3", df$video_file) ~ "BGL4",
                                  grepl("16_tol2_13", df$video_file) ~ "BGL5",
                                  grepl("16_tol2_14", df$video_file) ~ "BGL6",
                                  grepl("04_tol2_4", df$video_file) ~ "BGL7",
                                  grepl("18_tol1_2", df$video_file) ~ "BGL8", 
                                  grepl("21_tol3_12", df$video_file) ~ "Control1", 
                                  grepl("21_tol3_11", df$video_file) ~ "Control2", 
                                  grepl("07_tol3_7", df$video_file) ~ "Control3",
                                  grepl("01_TOL4_15", df$video_file) ~ "Control4", 
                                  grepl("13_tol3_1", df$video_file) ~ "Control5", 
                                  grepl("12_tol1_5", df$video_file) ~ "Control6", 
                                  grepl("12_tol1_2", df$video_file) ~ "Control7", 
                                  grepl("23_tol1_10", df$video_file) ~ "Control8",TRUE ~ "m"),
                video_f = as.factor(video))
}




df_pb <- f_video(df_pb)
fr_pb <- read_delim(frfile,"\t", escape_double = FALSE, locale =
                       locale(decimal_mark = ".", grouping_mark = "'"), trim_ws = TRUE)




FIX_ID_df <- function(df) {
    #is.na(as.numeric(df$RIGHT_FIX_INDEX))
    df$RIGHT_FIX_INDEX[df$RIGHT_FIX_INDEX=='.'] <- 0
    df$LEFT_FIX_INDEX[df$LEFT_FIX_INDEX=='.'] <- 0
    df["CURRENT_FIX_INDEX"] <- NA
    df$CURRENT_FIX_INDEX <- as.numeric(df$RIGHT_FIX_INDEX) + as.numeric(df$LEFT_FIX_INDEX)
    df$CURRENT_FIX_INDEX[df$CURRENT_FIX_INDEX==0] <- NA

    return(df)
}

df_pb <- FIX_ID_df(df_pb)




f.merge0 <- function(df, fr) {
  df.temp <- merge(df, fr, by=c("RECORDING_SESSION_LABEL","TRIAL_INDEX","IP_INDEX","IP_LABEL","CURRENT_FIX_INDEX"),
                   all.x = TRUE)
  index <- with(df.temp, order(TRIAL_INDEX, SAMPLE_INDEX))
  df.temp<- df.temp[index,]  
  df.temp                    
}

df_pb <- f.merge0(df_pb, fr_pb)

f.merge <- function(df) {
  df.temp <- merge(df, df_vidco, by.x = c("video", "frame"), by.y = c("video", "frames2"), all.x = TRUE)
  index <- with(df.temp, order(TRIAL_INDEX, SAMPLE_INDEX))
  df.temp<- df.temp[index,]
  df.temp
}

m.df_pb <- f.merge(df_pb)

save(m.df_pb, file = outfile)
rm(list=ls())
gc()
print("Preprocess done")
print("-------------------------------------------------")


