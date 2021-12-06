import matplotlib.pyplot as plt

def ratio_plot(data):
    a_star = data[data.name == 'A Star']
    idastar = data[data.name == 'IDAStar']
    fig, ax = plt.subplots(figsize=(10, 10), dpi=80)
    plt.style.use('ggplot')
    labels=['A Star','IDA Star']
    ax.boxplot([a_star.ratio,idastar.ratio])
    ax.set_title('Ratio Comparison of A* and IDA*',fontsize=24)
    ax.set_ylabel('Ratio (Generated/Expanded)',fontsize=18)
    ax.set_xticklabels(labels=labels, Fontsize=20)
    plt.ylim(0, 3)
    fig.savefig("ratio.jpg")

def node_plot(data):
    a_star = data[data.name == 'A Star']
    idastar = data[data.name == 'IDAStar']
    plt.style.use('ggplot')
    fig, ax = plt.subplots(ncols=2,figsize=(30, 15), dpi=80)
    ax[0].scatter(idastar.time_ms,idastar.generated,label='IDA*')
    ax[0].scatter(a_star.time_ms,a_star.generated,label='A*')
    ax[0].legend(loc=2,fontsize=18)
    ax[0].set_title('Generated Nodes',fontsize=24)
    ax[0].set_ylabel('Nodes',fontsize=20)
    ax[0].set_xlabel('Time (milliseconds)',fontsize=20)
    # idastar.time_ms,idastar.generated
    ax[1].scatter(a_star.time_ms,a_star.expanded,label='IDA*')
    ax[1].scatter(idastar.time_ms,idastar.expanded,label='A*')
    ax[1].legend(loc=2,fontsize=18)
    ax[1].set_title('Expanded Nodes',fontsize=24)
    ax[1].set_xlabel('Time (milliseconds)',fontsize=20)
    plt.ylim(0, 6000)
    fig.suptitle('Comparison of A* and IDA*',fontsize=30)
    fig.savefig("node_plot.png")