# -*- coding: utf-8 -*-

import JSONHelper, FileHelper

paths = ["..\\ML-Text-Project DATA\\ISKurasov.json",
         "..\\ML-Text-Project DATA\\AVSafeeva.json",
         "..\\ML-Text-Project DATA\\DVFilyanin.json"]

output = "..\\ML-Text-Project DATA\\allReviews.json"

data = JSONHelper.mergeFiles(paths, output)