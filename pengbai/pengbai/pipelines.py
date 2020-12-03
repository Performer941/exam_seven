# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import os

from itemadapter import ItemAdapter


class PengbaiPipeline:
    def process_item(self, item, spider):
        # 判断是否存在download文件夹，如果没有则创建
        download_path = os.getcwd() + './images/'  # 当前文件夹下的download文件夹
        if not os.path.exists(download_path):  # 判断文件夹或文件
            os.makedirs(download_path)

        if item.get("type") == "text":
            item.pop("type")
            with open("pengbai.csv", "a+", encoding="utf-8") as f:
                f_csv = csv.DictWriter(f, ["title", "title_url"])
                f_csv.writerows([item])

        elif item.get("type") == "img":
            item.pop("type")
            print("----------------------------------------------", item.get("img"))
            with open(item.get("img_name"), "wb") as f:
                f.write(item.get("img"))

        # return item
