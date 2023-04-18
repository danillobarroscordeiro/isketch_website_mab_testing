from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import beta
from scipy.stats import norm


def bayesian_inference(data):
    N_mc = 10000
    proba_b_better_a = []
    expected_loss_a = []
    expected_loss_b = []
    for day in range (len(data)):
        u_a, var_a = beta.stats(a = 1 + data.loc[day, 'acc_click_A'],
                                      b = 1 + (data.loc[day,'acc_visit_A'] -  data.loc[day, 'acc_click_A']),
                                      moments = 'mv'
        )
        
        u_b, var_b = beta.stats(a = 1 + data.loc[day, 'acc_click_B'],
                                      b = 1 + (data.loc[day,'acc_visit_B'] -  data.loc[day, 'acc_click_B']),
                                      moments = 'mv'
        )
        
        # Sampling of a normal distribution using u_a and var_a
        x_a = np.random.normal(loc = u_a,
                               scale = 1.25*np.sqrt(var_a),
                               size = N_mc
        )

         # Sampling of a normal distribution using u_b and var_b
        x_b = np.random.normal(loc = u_b,
                               scale = 1.25*np.sqrt(var_b),
                               size = N_mc
        )

        # Beta distribution function of page A
        pdf_beta_a = beta.pdf(x_a,
                            a = 1 + data.loc[day, 'acc_click_A'],
                            b = 1 + (data.loc[day,'acc_visit_A'] -  data.loc[day, 'acc_click_A'])
        )

        pdf_beta_b = beta.pdf(x_b,
                            a = 1 + data.loc[day, 'acc_click_B'],
                            b = 1 + (data.loc[day,'acc_visit_B'] -  data.loc[day, 'acc_click_B'])
        )

        # Normal distribution function of page A
        pdf_normal_a = norm.pdf(x_a,
                                      loc = u_a,
                                      scale = 1.25*np.sqrt(var_a)
        )

         # Normal distribution function of page B
        pdf_normal_b = norm.pdf(x_b,
                                      loc = u_b,
                                      scale = 1.25*np.sqrt(var_b)
        )

        # Beta / Normal
        y = (pdf_beta_a*pdf_beta_b) / (pdf_normal_a*pdf_normal_b)

        # Values where B is better than A
        y_b = y[x_b >= x_a]

        # Probability of B being A
        p = (1 / N_mc) * np.sum(y_b)

        # Expected error
        expected_loss_A = (1/N_mc) * np.sum(((x_b - x_a) * y)[x_b >= x_a])
        expected_loss_B = (1/N_mc) * np.sum(((x_a - x_b) * y)[x_a >= x_b])

        proba_b_better_a.append(p)
        expected_loss_a.append(expected_loss_A)
        expected_loss_b.append(expected_loss_B)

    return proba_b_better_a, expected_loss_a, expected_loss_b

def animate( i ):
    data = pd.read_csv('data_experiment.csv')

    # dtypes
    data['click'] = data['click'].astype(int)
    data['visit'] = data['visit'].astype(int)

    data = data.reset_index().rename(columns={'index':'day'})
    data = data.pivot(index='day', columns='group', values=['click', 'visit']).fillna(0)
    data.columns = ['click_control', 'click_treatment','visit_control', 'visit_treatment']
    data = data.reset_index(drop=True)

    data['acc_visit_A'] = data['visit_control'].cumsum()
    data['acc_click_A'] = data['click_control'].cumsum()
    data['acc_visit_B'] = data['visit_treatment'].cumsum()
    data['acc_click_B'] = data['click_treatment'].cumsum()

    # inference bayesian
    p, expected_loss_a, expected_loss_b = bayesian_inference(data)

    x1 = np.arange(len(p))
    

    plt.cla()
    plt.plot(x1,p, label='Probability B better A')
    plt.plot(x1,expected_loss_a, label='Risk Choosing A')
    plt.plot(x1,expected_loss_b, label='Risk Choosing B')

    plt.legend(loc='upper left')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval=1000)  

plt.tight_layout()
plt.show()