import requests
from bs4 import BeautifulSoup

# 浏览器代{过}{滤}理
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
}


# 获取该url地址下的源码
def get_url(url):
    data = requests.get(url, headers=headers).content.decode("utf-8")
    # 使用html5lib 容错率较高
    soup = BeautifulSoup(data, "html5lib")
    return soup


# 通过网页源码匹配该地区的七天天气的html源码
def gain_data(soup):
    hanmls = soup.find("div", class_="hanml")
    # 匹配到存放所有天数温度的div标签下的数据
    conmidtabs = hanmls.find_all("div", class_="conMidtab")
    return conmidtabs


# 通过网页源码匹配是哪七天
def gain_day():
    url = "http://www.weather.com.cn/textFC/hb.shtml"
    soup = get_url(url)
    day = []
    days = list(soup.find("ul", class_="day_tabs").stripped_strings)
    for Current in days:
        day.append(Current)
    return day


# 获取每天的数据
def gain_table(conmidtab):
    tabs = conmidtab.find_all("table")
    # 用来存放遍历的数据
    y = {}
    # 遍历当天该地区的所有城市
    for tab in tabs:
        # 因为前两个是表头 所以从第三个获取每个省的城市的名字和温度
        trs = tab.find_all("tr")[2:]

        for tr in trs:
            citys = list(tr.find("td", width="83").stripped_strings)[0]
            low_tmps = list(tr.find("td", width="86").stripped_strings)[0]

            cloud = list(tr.find("td", width="89").stripped_strings)[0]
            wind = list(tr.find("td", width="162").stripped_strings)[0]
            high_tmps = list(tr.find("td", width="92").stripped_strings)[0]


            y[citys] = {
                'min_temp':low_tmps,
                'max_temp':high_tmps,
                'cloud':cloud,
                'wind':wind
            }
            # 把字典y中的数据存放到该数组中
    return y


# 把数据到本地
def write_file(regions, lis1_index):
    lis1 = ["华北", "东北", "华东", "华中", "华南", "西北", "西南", "港澳台"]
    with open("./中国天气.txt", "a", encoding="utf-8") as fp:
        for keys, values in regions.items():
            fp.write((lis1[lis1_index] + "\t"))
            fp.write((keys + "\t"))
            for key, value in values.items():
                fp.write((key + "-" + str(value) + "\t"))
            fp.write("\n")


if __name__ == '__main__':
    # 用来存放该地区七天的温度
    current_temperature = []
    partitions = ["hb", "db", "hd", "hz", "hn", "xb", "xn", "gat"]
    prefix = "http://www.weather.com.cn/textFC/"
    # 获取七天的日期 days是个列表
    days = gain_day()
    regions = {}
    lis1_index = 0
    # 遍历 所有的地区 华北，华东等等
    for partition in partitions:
        url = prefix + partition + ".shtml"
        # 调用get_url获取源码
        soup = get_url(url)
        # 调用gain_data 获取到七天天气的源码
        conmidtabs = gain_data(soup)
        # 作为days数组的下标
        day_index = 0
        # 把七天的数据依次传递 获取每天的数据
        for conmidtab in conmidtabs:
            data = gain_table(conmidtab)
            regions[days[day_index]] = data
            day_index += 1

        write_file(regions, lis1_index)
        lis1_index += 1
