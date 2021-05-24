from gc import collect
from pandas import DataFrame


class Query:
    @staticmethod
    def perform_query(pageviews):
        # initializes dataframe from PageView list (All hours)
        df_hours = DataFrame(pageviews,
                             columns=['domain_code',
                                      'page_title', 'count_views'])
        # sets dtype to minimize memory usage
        df_hours = df_hours.astype(dtype={'domain_code': 'object',
                                          'page_title': 'object',
                                          'count_views': 'uint16'})
        # sets query a
        groupedby_a = df_hours.groupby(['domain_code', 'page_title'])
        query_a = groupedby_a['count_views'].sum().reset_index(name='cnt')
        # sets query b (same as a)
        query_b = query_a.copy()
        # collects garbage
        Query._collect_gb([df_hours, groupedby_a, query_a])
        # sets query c
        query_c = query_a.groupby('domain_code')['cnt'].max().reset_index(
            name='max_count_views')
        # inner joins query b and query c
        join_r = query_b.join(query_c.set_index(
            ['domain_code', 'max_count_views']),
            how='inner', on=['domain_code', 'cnt']
        ).reset_index(drop=True)
        # collects garbage
        Query._collect_gb([query_b, query_c])
        # sets query r
        query_r = join_r.sort_values(by='cnt',
                                     ascending=False).rename(
                                         columns={'cnt': 'max_count_views'})
        # sets final result
        final_result = query_r.head(100).reset_index(drop=True)
        # collects garbage
        Query._collect_gb([join_r, query_r])

        return final_result

    @staticmethod
    def _collect_gb(dfs):
        # deletes variables and calls garbage collector
        for df in dfs:
            del(df)
        collect()
