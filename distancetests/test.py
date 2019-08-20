def merge0txt():
    for i in range(4,54):
        print("df_pb"+str(i)+" <- FIX_ID_df(df_pb"+str(i)+")")
        print("df_pb"+str(i)+" <- f.merge0(df_pb"+str(i)+", fr_pb"+str(i)+")")

def frtxt():
    for i in range(5,54):
        print("fr_pb"+str(i)+"<- read_delim(\"data/fr_"+str(i)+".xls\",\"\t\", escape_double = FALSE, locale = \n "
                "locale(decimal_mark = \".\", grouping_mark = \"'\"), trim_ws = TRUE)")

