import unittest

from aiops.learnware.MachineLearnware import MachineLearnware


class testMachineLearnware(unittest.TestCase):

    def testSelectModel(self):

        import pandas as pd
        import matplotlib.pyplot as plt
        chunks = []
        chunkSize = 100 * 10
        chunk = pd.read_csv('D:/ProgramData/machine_usage.csv', chunksize=chunkSize,
                            names=['machine_id', 'timestamp', 'cpu_util_percent', 'mem_util_percent', 'mem_gps', 'mkpi',
                                   'net_in', 'net_out', 'disk_io_percent'])
        for i in range(0, 200):
            chunks.append(chunk.get_chunk(chunkSize))

        df = pd.concat(chunks, ignore_index=True)
        df['event_time'] = pd.to_datetime(df['timestamp'], unit="s")
        df = df.sort_values('event_time')
        df = df.set_index('event_time')

        test0 = pd.DataFrame(df[df['machine_id'] == "m_1932"]['cpu_util_percent'])
        test1 = pd.DataFrame(df[df['machine_id'] == "m_1933"]['cpu_util_percent'])
        test2 = pd.DataFrame(df[df['machine_id'] == "m_1934"]['cpu_util_percent'])
        test3 = pd.DataFrame(df[df['machine_id'] == "m_1935"]['cpu_util_percent'])
        test4 = pd.DataFrame(df[df['machine_id'] == "m_1936"]['cpu_util_percent'])
        test5 = pd.DataFrame(df[df['machine_id'] == "m_1937"]['cpu_util_percent'])
        test6 = pd.DataFrame(df[df['machine_id'] == "m_1938"]['cpu_util_percent'])
        test7 = pd.DataFrame(df[df['machine_id'] == "m_1939"]['cpu_util_percent'])

        test0['diff'] = test0['cpu_util_percent'].diff().fillna(0)
        test1['diff'] = test1['cpu_util_percent'].diff().fillna(0)
        test2['diff'] = test2['cpu_util_percent'].diff().fillna(0)
        test3['diff'] = test3['cpu_util_percent'].diff().fillna(0)
        test4['diff'] = test4['cpu_util_percent'].diff().fillna(0)
        test5['diff'] = test5['cpu_util_percent'].diff().fillna(0)
        test6['diff'] = test6['cpu_util_percent'].diff().fillna(0)
        test7['diff'] = test7['cpu_util_percent'].diff().fillna(0)

        learnware = MachineLearnware()
        result0 = learnware.call("cpu_util_percent", "m_1932", test0.values)
        result1 = learnware.call("cpu_util_percent", "m_1933", test1.values)
        result2 = learnware.call("cpu_util_percent", "m_1934", test2.values)
        result3 = learnware.call("cpu_util_percent", "m_1935", test3.values)
        result4 = learnware.call("cpu_util_percent", "m_1936", test4.values)
        result5 = learnware.call("cpu_util_percent", "m_1937", test5.values)
        result6 = learnware.call("cpu_util_percent", "m_1938", test6.values)
        result7 = learnware.call("cpu_util_percent", "m_1939", test7.values)

        test0['predict'] = result0
        test1['predict'] = result1
        test2['predict'] = result2
        test3['predict'] = result3
        test4['predict'] = result4
        test5['predict'] = result5
        test6['predict'] = result6
        test7['predict'] = result7

        plt.subplot(4, 2, 1)
        test0["cpu_util_percent"].plot(zorder=1, figsize=(12, 8))
        plt.scatter(x=test0[test0["predict"] == -1].index,
                    y=test0[test0["predict"] == -1]["cpu_util_percent"], c="red", zorder=2)

        plt.subplot(4, 2, 2)
        test1["cpu_util_percent"].plot(zorder=1, figsize=(12, 8))
        plt.scatter(x=test1[test1["predict"] == -1].index,
                    y=test1[test1["predict"] == -1]["cpu_util_percent"], c="red", zorder=2)

        plt.subplot(4, 2, 3)
        test2["cpu_util_percent"].plot(zorder=1, figsize=(12, 8))
        plt.scatter(x=test2[test2["predict"] == -1].index,
                    y=test2[test2["predict"] == -1]["cpu_util_percent"], c="red", zorder=2)

        plt.subplot(4, 2, 4)
        test3["cpu_util_percent"].plot(zorder=1, figsize=(12, 8))
        plt.scatter(x=test3[test3["predict"] == -1].index,
                    y=test3[test3["predict"] == -1]["cpu_util_percent"], c="red", zorder=2)

        plt.subplot(4, 2, 5)
        test4["cpu_util_percent"].plot(zorder=1, figsize=(12, 8))
        plt.scatter(x=test4[test4["predict"] == -1].index,
                    y=test4[test4["predict"] == -1]["cpu_util_percent"], c="red", zorder=2)

        plt.subplot(4, 2, 6)
        test5["cpu_util_percent"].plot(zorder=1, figsize=(12, 8))
        plt.scatter(x=test5[test5["predict"] == -1].index,
                    y=test5[test5["predict"] == -1]["cpu_util_percent"], c="red", zorder=2)

        plt.subplot(4, 2, 7)
        test6["cpu_util_percent"].plot(zorder=1, figsize=(12, 8))
        plt.scatter(x=test6[test6["predict"] == -1].index,
                    y=test6[test6["predict"] == -1]["cpu_util_percent"], c="red", zorder=2)

        plt.subplot(4, 2, 8)
        test7["cpu_util_percent"].plot(zorder=1, figsize=(12, 8))
        plt.scatter(x=test7[test7["predict"] == -1].index,
                    y=test7[test7["predict"] == -1]["cpu_util_percent"], c="red", zorder=2)
        plt.show()




if __name__ == '__main__':
    unittest.main()