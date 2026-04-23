'''just a quick plot showing the increase of CRC during the years'''
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 24})

df = pd.read_csv("NumberCRC_InTokens.csv")

df["Date"]=pd.to_datetime(df["Date"],format='%d/%m/%y') 

from matplotlib.ticker import MaxNLocator

ax = plt.figure().gca()
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.plot(df["Date"],df["NumberCRC"],"bo",label="registered CRCs")
ax.set_xlabel("Date")
ax.set_ylabel("Number of registered CRCs")
ax.plot([pd.to_datetime("01/06/23",format='%d/%m/%y'),pd.to_datetime("01/06/23",format='%d/%m/%y')],[0,24],"r--",label="start of CTA+ project")
plt.legend()
plt.show()