import matplotlib as mpl
import matplotlib.pyplot as plt
import si_prefix as si


# Format float values as string w.r.t. amps, e.g., `A`, `mA`, `uA`, etc.
A_formatter = mpl.ticker.FuncFormatter(lambda x, pos:
                                       '{}A'.format(si.si_format(x)))


def plot_microdrop_dstat_data(df_data, axis=None):
    '''
    Plot Microdrop DStat experiment current measurement results, grouped by
    experiment uuid, step label (or number), and step attempt number.

    Args
    ----

        df_data (pandas.DataFrame) : Microdrop DStat experiment results with at
            least the columns `experiment_uuid`, `step_number`, `step_label`,
            `attempt_number`, `time_s`, and `current_amps`.
        axis (matplotlib.axes._subplots.AxesSubplot) : Axis to plot onto.  If
            `None`, an axis is automatically created.

    Returns
    -------

        (matplotlib.axes._subplots.AxesSubplot) : Matplotlib axis.  Useful, for
            example, to perform further axis customization, etc.
    '''
    if axis is None:
        fig, axis = plt.subplots(figsize=(12, 4))

    # Make copy of data since we modify it.
    df_data = df_data.copy()
    df_data.loc[:, 'step_label'] = df_data.loc[:, 'step_label'].fillna('')

    for (experiment_uuid_i, step_number_i,
         attempt_number_i), df_i in df_data.groupby(['experiment_uuid',
                                                     'step_number',
                                                     'attempt_number']):
        step_label_i = df_i.step_label.iloc[0]
        step_label_i = (step_label_i if step_label_i else
                        'step{:03d}'.format(step_number_i))

        label_i = '[{}]-{}-{:02d}'.format(experiment_uuid_i[:8], step_label_i,
                                          attempt_number_i)
        # Get style properties to use for plot `i`.
        props_i = axis._get_lines.prop_cycler.next()
        # Plot measured DStat current at each time point.
        df_i.set_index('time_s').current_amps.plot(ax=axis, label=label_i,
                                                   **props_i)

        # Compute median measured current.  The median helps to eliminate
        # outliers.
        median_i = df_i.current_amps.median()
        # Plot median as a straight line.
        axis.plot(axis.get_xlim(), 2 * [median_i], linewidth=2, **props_i)
        axis.legend()
    #     # Annotate the median with the name of the sample.
    #     axis.text(axis.get_xlim()[0], median_i, label_i, fontsize=14,
    #               color='black')

    # Format y-axis tick labels to be like `1.0nA`, `3.7mA`, etc.
    axis.yaxis.set_major_formatter(A_formatter)
    return axis
