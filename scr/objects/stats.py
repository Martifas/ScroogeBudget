import datetime
import csv
import pandas as pd
import os
import plotly.express as px
from scr.objects.username import read_profile_file
from scr.menu.utilities import menu_compiler


class Stats:
    def __init__(self, username):
        self.username = username
        self.transactions_data = read_profile_file(self.username, transactions=True)[0]


    def stats_menu(self):
        modes = ["Income/expense stats", "Savings stats"]
        output_string = "STATISTICS MENU"
        menu_compiler(modes, output_string)


    def extract_monthly_amount(self, transaction_type):
        data = {}
        for row in self.transactions_data:
            if row[0] == transaction_type:
                date_obj = datetime.datetime.strptime(row[1], "%Y-%m-%d").date()
                year_month = date_obj.strftime("%Y-%m")
                amount = int(row[2])
                if year_month in data:
                    data[year_month] += amount
                else:
                    data[year_month] = amount

        data_list = [[key, value] for key, value in data.items()]
        return data, data_list

    def compile_stats(self):
        data_list = self.savings_stats()[1]
        self.show_stats(data_list)
        message = "Showing stats in browser"
        return message

    def income_stats(self):
        data, data_list = self.extract_monthly_amount("Income")
        return data, data_list

    def savings_stats(self):
        data, data_list = self.extract_monthly_amount("Savings")
        return data, data_list

    def show_stats(self, data_list) -> None:
        df = pd.DataFrame(data_list, columns=["YearMonth", "Amount"])
        total_amount = df["Amount"].sum()
        fig = px.bar(
            df,
            x="YearMonth",
            y="Amount",
            title="Savings Over Time",
            color="Amount",
            color_continuous_scale=px.colors.sequential.Viridis,
        )
        fig.update_layout(
            xaxis_title="Year and Month",
            yaxis_title="Amount Saved",
        )
        fig.update_traces(texttemplate="%{y}", textposition="outside")
        fig.update_yaxes(range=[0, df["Amount"].max() * 1.1])
        fig.add_annotation(
            x=0.5,
            y=-0.2,
            xref="paper",
            yref="paper",
            text=f"Total Amount Saved: {total_amount}",
            showarrow=False,
            font=dict(size=14),
            align="center",
        )
        fig.show()
