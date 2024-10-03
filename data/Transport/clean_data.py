import pandas as pd
import matplotlib.pyplot as plt
import country_converter as coco
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

countries_path = os.path.join(current_dir, '..', 'countries.csv')
public_transport_path = os.path.join(current_dir,'public_transport.csv')


df = pd.read_csv(countries_path)
result_transport = pd.read_csv(public_transport_path)
