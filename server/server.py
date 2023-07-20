from knowknow import *
import streamlit as st

from load_db import db

dbs = [
    ("Sociology (WoS; as in McGail 2021)", db),
    #("Sociology (WoS; full unfiltered db)", Dataset('sociology-wos-all')),
    #("Sociology (WoS; self-citations removed)", Dataset('sociology-wos-74b-noself')),
]
names = [x[0] for x in dbs]
dbs = [x[1] for x in dbs]


st.sidebar.markdown("""All code for replication and extension of these results are available [on GitHub](https://github.com/amcgail/lost-forgotten). You can find the paper which spawned this interface [in *The American Sociologist*](https://link.springer.com/article/10.1007/s12108-021-09490-4).""")

db_sel = st.sidebar.selectbox("Choose your dataset (more to be added soon).", range(len(dbs)), format_func=lambda x:names[x] )
db = dbs[db_sel]

def get_table_download_link(df):
    import base64

    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href

def top_app():
    dta = Dataset('sociology-wos-74b')

    st.markdown("""
    # top cited works of all time
    """)

    typ_o = [
        "Top N in each decade",
        "Top % in each decade",
    ]

    typ = st.sidebar.selectbox("How to determine the top?", typ_o)
    yStart = st.sidebar.selectbox("How early to include?", [1900, 1940, 1970], index=1)
    if typ == typ_o[0]:
        topN = st.sidebar.selectbox("Top N in each decade", [20,50,100])
        maxP = st.sidebar.selectbox("Upper limit on total proportional citations", [None,0.10,0.25], index=2)
        args=(db_sel, typ_o.index(typ), yStart, topN, maxP)
        mkit=lambda: stats.top_decade_stratified(dta, 'c', topN=topN, maxP=maxP, debug=False, yRange=(yStart,2015))

        f"""
        This method takes the top N documents in each decade, rolling through the start (you have {yStart} - {yStart+10} selected) to 2005-2015.
        It eliminates duplicates, and records the date in which each work first appeared in the top N list, along with various other attributes of the cited work.
        """
    elif typ == typ_o[1]:
        topP = st.sidebar.selectbox("Top % in each decade", [0.1,0.05,0.02,0.01], index=3, format_func=lambda x:f"{x:0.0%}")
        args=(db_sel, typ_o.index(typ), yStart, topP)
        mkit=lambda: stats.top_decade_stratified(dta, 'c', percentile=topP, yRange=(yStart,2005), debug=False)

        f"""
        This method takes the top documents by percentile in each decade, rolling through the start (you have {yStart} - {yStart+10} selected) to 2005-2015.
        It eliminates duplicates, and records the date in which each work first appeared in the top % list, along with various other attributes of the cited work.
        """


    #srt = st.sidebar.selectbox

    import pickle

    topf = Path("top_df_%s.pickle" % str(args))

    if topf.exists():
        with topf.open('rb') as inf:
            top_df = pickle.load(inf)
    else:
        loading_state = st.text('Not yet computed... Working...')
        top_df = mkit()
        loading_state.text('Done...')
        with topf.open('wb') as outf:
            pickle.dump(top_df, outf)

    tops = Counter([x.split("|")[0] for x in top_df['name']]).most_common(30)
    tops_c = Counter([x[1] for x in tops])
    top_a_n = max(tops_c)

    top_as = [x[0] for x in tops if x[1] == top_a_n]
    top_a = ", ".join( top_as[:-1] ) + " & "*( len(top_as) > 1 ) + top_as[-1]

    f"""
    + {top_df[top_df.type=='book'].shape[0]:,} books and {top_df[top_df.type=='article'].shape[0]:,} articles, {top_df.shape[0]:,} in total.
    + `{top_a}` occurred the most, with {top_a_n} docs in the list.
    """

    st.dataframe(top_df.sort_values('total', ascending=False))

    """Use the following link to download this table for your own purposes.
    """
    st.markdown(get_table_download_link(top_df), unsafe_allow_html=True)


def author_app():

    N_pubs = st.sidebar.selectbox("Show top N publications", [20,50,100])

    def key2name(tname, truncate=None):
        tstr = tname.split("|")
        if len(tstr) == 3:
            tstr = "%s (%s)\n%s" % (tstr[0], tstr[1], tstr[2])
        else:
            if False and tname in dd:
                yy = dd[tname][2]
            else:
                yy = db.trend('c', tname).first
            tstr = "%s (%s*)\n%s" % (tstr[0], yy, tstr[1])
        tstr = tstr.lower()
        return tstr

    import matplotlib
    @st.cache(hash_funcs={matplotlib.figure.Figure: lambda _: None})
    def author_fig_old(K, limit=None, db_i=None):
        pubs = db.search('c',"%s|"%K)

        pubs = sorted(pubs, key=lambda x:-db(c=x).cits)
        if limit is not None:
            pubs = pubs[:limit]

        viz.yearly_counts_table(db,
            pubs,
            NCOLS=2,
            yearlim=(1950,2015),
            tickstep=20,
            print_names={
                x: key2name(x)#"%s\n%s".join( x.split("|")[1:] )[:30] + "..."
                for x in pubs
            },
            #markranges={
            #    x:first_r(x)
            #    for x in pubs
            #}
        )
        #plt.title("Talcott Parsons")
        return plt.gcf()

    def author_fig(K, limit=None, db_i=None):
        pubs = db.search('c',"%s|"%K)

        pubs = sorted(pubs, key=lambda x:-db(c=x).cits)
        if limit is not None:
            pubs = pubs[:limit]

        #mk = {r['name']:(r.first_added,r.first_added+10) for i,r in top_df.iterrows()}
        mk = {}
        viz.yearly_counts_table_simp(db, pubs, NCOLS=3, print_names={k:key2name(k) for k in pubs}, markranges=mk, yearlim=(1940,2015))
        #plt.savefig('top20.longer.%s.png'%i)
        return plt.gcf()

    st.markdown('# Author investigations')
    srch = st.text_input('Enter the author you want to investigate (Last, F.)')

    def display_auth(WHO):


        st.markdown(f"# {WHO}")
        st.write("## top cited works")
        st.write( author_fig(WHO, limit=N_pubs, db_i=db_sel) )
        st.markdown(f"&ast; Indicates that there is no definitive publication year (mostly for books), and instead the year of first publication is shown.")

        st.write("## which journals most cite them")
        res = db(ta=WHO, fj=None).cits.sort_values('count', ascending=False).head(10)
        st.dataframe(res)

    if srch != "":
        res_c = db.search('c', srch)
        res_ta = db.search('ta', srch)

        st.markdown(f"""
    + {len(res_ta)} author{'s' if len(res_ta)>1 else ''} found ({"; ".join(res_ta)})
    + {len(res_c)} publications found
        """)

        for a in res_ta:

            display_auth(a)



def data_app():

    cc = db.by('c').cits

    num1 = sum([1 for x,c in cc.items() if c == 1])
    num2 = sum([1 for x,c in cc.items() if c in [2,3,4]])
    num3 = sum([1 for x,c in cc.items() if 15 >= c >= 5])
    num4 = sum([1 for x,c in cc.items() if 100 >= c >= 15])
    num5 = sum([1 for x,c in cc.items() if 100 <= c ])

    total = sum([1 for x,c in cc.items() if c >= 1])

    ys = [x[0] for x in db.by('fy').cits.keys()]

    f"""# summary statistics

    + {len(db.by('fj').cits):,} journals
    + {len(db.by('ta').cits):,} cited authors
    + {len(db.by('fa').cits):,} citing authors
    + {total:,} cited books and articles
        + {num1:,} with 1 citation
        + {num2:,} with 2-4 citations
        + {num3:,} with 5-15 citations
        + {num4:,} with 15-100 citations
        + {num5:,} with 100+ citations
    + {max(ys)-min(ys)+1:,} years of citations
    """

    c = db.by('fy').cits
    yrs = range(1900,2010,1)
    plt.plot(yrs, np.log([c[(y,)] for y in yrs]));
    plt.title('Log(# citations) by year')
    st.write(plt.gcf())

apps = [
    {
        'title': 'Search Authors',
        'function': author_app
    },
    {
        'title': 'Dataset summary',
        'function': data_app
    },
    {
        'title': 'Top in each decade, stratified',
        'function': top_app
    }
]

app = st.sidebar.radio(
            'Go To',
            apps,
            format_func=lambda app: app['title'])

app['function']()

from foot import footer
footer()
