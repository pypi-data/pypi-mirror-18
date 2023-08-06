import quorra
import pandas

df = pandas.DataFrame({'size': [1,2,3,1,2,3], 'rfu': [1,2,3,5,6,7], 'channel': ['fam', 'fam', 'fam', 'ned', 'ned', 'ned']})

plt = quorra.line()\
    .data(df, x='size', y='rfu', group='channel')\
    .opacity(0.75).lposition("outside")\
    .lshape("circle").labelposition("end")

quorra.export(plt, 'tmp.png')
