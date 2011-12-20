# Scrapy settings for what project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'what'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['what.spiders']
NEWSPIDER_MODULE = 'what.spiders'
DEFAULT_ITEM_CLASS = 'what.items.WhatItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = ['what.pipelines.WhatPipeline']

