import pandas as pd
import numpy as np

newport = "7762"

dftot = pd.read_csv("/home/antonio/OCRA/CRC_monitoring/crc_summary/CRCNetwork_status_report.csv", index_col="Time")
dftot[newport] = 0

dftot.to_csv("/home/antonio/OCRA/CRC_monitoring/crc_summary/CRCNetwork_status_report_updated.csv")

