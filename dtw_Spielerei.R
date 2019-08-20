
library(dtw)


load("S:/Buchholz/Gaze Pursuit/data_kl/pb2.Rda")
prep_df <- function(df) {
  df$x_coord[df$x_coord == 0] <- NA
  df$y_coord[df$y_coord == 0] <- NA
  if (is.character(df$LEFT_GAZE_X)) {
    df$eye.x <- as.numeric(df$RIGHT_GAZE_X)
    df$eye.y <- as.numeric(df$RIGHT_GAZE_Y)
  }
  else {
    df$eye.x <- as.numeric(df$LEFT_GAZE_X)
    df$eye.y <- as.numeric(df$LEFT_GAZE_Y)
  }
  return(df)
}

m.df <- prep_df(m.df_pb2)
#m.df <- m.df_pb1
rm(m.df_pb2)
gc()
m.df$block.f <- as.factor(m.df$block)

m.df <- subset(m.df, (!is.na(m.df$eye.x) & !is.na(m.df$eye.y) & !is.na(m.df$x_coord) & !is.na(m.df$y_coord)))
                         
sub_spot <- subset(m.df, video == "Spot2")

rm(query)
rm(ref)
gc()
                                                  
query <- cbind(sub_spot$CURRENT_FIX_X, sub_spot$CURRENT_FIX_Y)
ref <- cbind(sub_spot$x_coord, sub_spot$y_coord)
write.csv(query, file = "query.csv")
write.csv(ref, file = "ref.csv")
summary(pr_DB)

#####
start.time <- Sys.time()
alignment <- dtw(query[c(1500,2500),],ref[c(1500,2500),])
end.time <- Sys.time()
time.taken <- end.time - start.time
time.taken
alignment$distance
#####
dtw(query[c(1500,2500),],ref[c(1500,2500),],dist.method = "DTW",keep=TRUE)->alinment;
dtwPlotTwoWay(alignment,query,ref)
plot(alignment,offset=-2,type = "two",lwd=3, match.col = "grey50",match.indices=hi,main="Match lines shown every pi/4 on query");

alignment2 <- dtw(query,ref,dist.method="DTW", window.type = "sakoechiba", window.size = 1400)
alignment2$normapreplizedDistance
