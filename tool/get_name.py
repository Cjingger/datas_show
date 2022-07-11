import difflib
from xpinyin import Pinyin


class Get_name():
   def pipei(self,str1,str2):
      return  difflib.SequenceMatcher(None,str1,str2).quick_ratio()


   def pinyin(self,str):
      p = Pinyin()
      return p.get_pinyin(str).replace('-','')


   def get_name(self,l,email):

      l_ = []
      str2 = email.split('@')[0].lower()
      for i in l:
         str1 = self.pinyin(i.replace(' ','').replace(',','')).lower()
         l_.append(self.pipei(str1,str2))
      val = max(l_)  # 最大值
      if val:
         name = l[l_.index(val)]
      else:
         name = ';'.join(l[0:5])
      return name



