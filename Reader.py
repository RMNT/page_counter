import datetime as dt

class Reader():
  def __init__(self):
    self.all = 'all.txt'
    self.today = "today.txt"
    self.entered_today = 'entered_today.txt'
    self.read = 'read.txt'
    self.std_hours = 20
    self.day_of_the_week = dt.datetime.now().date().strftime('%A')[:3]
    self.pages = 100
    self.week_days = {'Mon':10, 'Tue':8, 'Wed':5, 'Thu':6, 'Fri':7, 'Sat':6, 'Sun':11}
    self.today_date = dt.datetime.now().date()
    self.date_str ='%Y-%m-%d'


  def create(self, file):
    f = open(file, 'w')
    f.close()


  def check_if_exists(self, file):
    exists = os.path.exists(file) 
    if exists:
      return exists
    self.create(file)


  def add_new_text(self, name:str, author:str, num_pages:int, deadline, subject):
    self.check_if_exists(self.all)
    
    with open(self.all, 'a') as f:
      f.write(f'{author} - {name}, {num_pages}, {deadline}, {subject}\n')
    
    self.sort_texts(self.all)


  def calc_days_left(self, l):
    date = dt.datetime.strptime(l[2], self.date_str).date()+ dt.timedelta(days=-2)
    diff = str(date - self.today_date)

    if "day" in diff:
      return int(diff.split(' ')[0])
    return 0


  def calc_pages_per_day(self, l):
    pages = l[1]
    days_left = self.calc_days_left(l)+1
    if days_left > 1:
      return int(round(int(pages)/days_left, 0))
    if days_left < 1:
      days_left = 1
    return int(round(int(pages)/days_left, 0))
    

  def sort_texts(self, file):
    texts = self.get_texts_list(file, datetime=True)
    texts.sort(key = lambda x: x[2])

    with open(self.all, 'w') as f:
      for t in texts:
        f.write(f'{t[0]}, {t[1]}, {str(t[2])}, {t[-1]}\n')

  def get_texts_list(self, file, datetime=False):
    texts = []
    
    with open(file, 'r') as f:
      lines = f.readlines()

    if file == self.today:
      lines = lines[1:]

    for l in lines:
      split = l.split(', ')
      if len(split) == 1:
        continue
      else:
        split[1] = int(split[1])
        if datetime:
          split[2] = dt.datetime.strptime(split[2], self.date_str).date()
        split[-1] = split[-1][:-1]
        texts.append(split)
    return texts


  def check_today_date(self):
    with open(self.today, 'r') as f:
      lines = f.readlines()
    
    if len(lines) == 0 or dt.datetime.strptime(lines[0][:-1], self.date_str).date() != self.today_date:
      return False
    return True


  def change_to_todays_date(self):
    with open(self.today, 'w') as f:
      f.write(str(self.today_date)+'\n')

  def update_was_today(self):
    # self.check_if_exists(self.entered_today)
    with open(self.today, 'r') as f:
      today_lines = f.readlines()[1:]

    author_text_list = [l[0] for l in today_lines]

    with open(self.entered_today, 'w') as f:
      for at in author_text_list:
        f.write(at+'\n')


  def was_today(self):
    self.check_if_exists(self.entered_today)
    
    with open(self.entered_today) as f:
      lines = f.readlines()
    
    if len(lines) > 0:
      return self.get_texts_list(self.entered_today)
    todays = self.get_texts_list(self.today_date)
    #baigt rašyt

  
  def update_was_today(self, list1, list2):
    # tekstų neišiminėt iš sąrašo, tik pridėti
    self.check_if_exists(self.entered_today)
    with open(self.all, 'r') as f:
      all_lines = [l.split(', ')[0] for l in f.readlines()]

    with open(self.today, 'r') as f:
      today_lines = [l.split(', ')[0] for l in f.readlines()[1:]]

    with open(self.entered_today, 'r') as f:
      entered = [l.split(', ')[0] for l in f.readlines()]

    new_texts = list(set(all_lines) - set(entered))


  def more_or_less_pages(self, lists):
    all_pages = sum([f[1] for f in lists])
    print(f'all pages: {all_pages}')
    hours = self.week_days[self.day_of_the_week]
    print(f'hours: {hours}')
    needed_hours = all_pages*self.std_hours/self.pages
    print(f'needed hours: {needed_hours}')

    if hours < needed_hours:
      print(f'lists: {lists}')
      print(f'lists len: {len(lists)}')
      print('Valandų mažiau nei reikia')
      other_today_texts = len(lists)-1
      
      diff = round(needed_hours - hours, 2)
      print(f'diff: {diff}')
      lost_pages = int(round(diff*self.pages/self.std_hours,0))
      print(f'lost_pages: {lost_pages}')
      
      earliest_deadline = lists[0][2]
      all_early_deadlines = len([ed for ed in lists if ed[2] == earliest_deadline])
      print(all_early_deadlines)

      index_list = [f for f in range(all_early_deadlines, len(lists))]

      index_sum = sum(index_list)

      one_part = round(lost_pages/index_sum, 2)
      part_of_lists = lists[all_early_deadlines:]
      print(part_of_lists)
      page_subtract = [int(round(f*one_part/1.8,0)) for f in index_list]
      print(page_subtract)
      
      to_del = []
      for ps, (i, lp) in zip(page_subtract, enumerate(part_of_lists)):
        if ps < lp[1]:
          lp[1] -= ps
        else:
          to_del.append(i+all_early_deadlines)

      print(f'to_del: {to_del}')      
      for i in to_del[::-1]:
        del lists[i]

    elif hours > needed_hours:
      print('Valandų daugiau nei reikia')
      diff = round(hours - needed_hours,2)
      print(f'diff: {diff}')
      can_add = int(round(diff*self.pages/self.std_hours, 0))
      print(f'can_add: {can_add}')
      all_closest_text_pages = int([f[1] for f in self.get_texts_list(self.all) if f[0] == lists[0][0]][0])
      print(f'all_closest_text_pages: {all_closest_text_pages}')
      other_closest_book_pages = all_closest_text_pages - lists[0][1]
      print(f'other_closest_book_pages')

      if can_add <= other_closest_book_pages:
        lists[0][1] += can_add
        print(f'lists[0][1]: {lists[0][1]}')
      else:
        print("TODO:Reiks ir iš kitos pridet")
    return lists

  def get_todays_reads(self):
    self.check_if_exists(self.today)
    self.check_if_exists(self.read)

    texts = self.get_texts_list(self.all)
    read_texts = [f[:-1] for f in open(self.read, 'r').readlines()]

    if not self.check_today_date():
      os.remove('read.txt')
      os.remove('today.txt')
      self.change_to_todays_date()

      today_reads = []
    
      for t in texts:
        if t[0] not in read_texts:
          pages = self.calc_pages_per_day(t)
          t[1] = pages
          today_reads.append(t)
      today_reads = self.more_or_less_pages(today_reads)

      with open(self.today, 'a') as f:
        for t in today_reads:
          f.write(t[0]+ ', ' + str(t[1]) +', '+ t[2] +', '+t[-1]+'\n')
          
      if len(today_reads) > 0:
        return today_reads
      else:
        print('Viskas perskaityta ^_^')

    else:
      today_texts = [f[:-1].split(',')[0] for f in open(self.today, 'r').readlines()[1:]]
      today_texts_full = [f[:-1] for f in open(self.today, 'r').readlines()[1:]]
    return today_texts_full


  def update_pages(self, author, text, read_pages):
    # jei nėra today.txt, sukurti jį
    author_text = author+' - '+ text

    with open(self.today, 'r') as f:
      today_lines = f.readlines()[1:]

    with open(self.all, 'r') as f:
      all_lines = f.readlines()
        
    today_authors = [f.split(', ')[0] for f in today_lines]
    all_authors = [f.split(', ')[0] for f in all_lines]

    if author_text in today_authors:
      today_idx = today_authors.index(author_text)
    else:
      today_idx = None

    if author_text in all_authors:
      all_idx = all_authors.index(author_text)
    else:
      print('Tekstas nerastas bendrame tekstų sąraše.')
      all_idx = None

    if today_idx != None:
      nl = today_lines[today_idx].split(', ')
      left_pages_today = int(nl[1]) - read_pages
      if left_pages_today > 0:
        today_line = f"{nl[0]}, {left_pages_today}, {nl[2]}, {nl[-1]}"
        today_lines[today_idx] = today_line
      else:
        self.write_to_read(nl[0])
        del today_lines[today_idx]
        
      with open(self.today, 'a') as f:
        self.change_to_todays_date()
        for tl in today_lines:
          f.write(tl)

    if all_idx != None:
      nla = all_lines[all_idx].split(', ')
      left_pages_all = int(nla[1]) - read_pages
      if left_pages_all > 0:
        new_all_line = f"{nla[0]}, {left_pages_all}, {nla[2]}, {nla[-1]}"
        all_lines[all_idx] = new_all_line
      else:
        del all_lines[all_idx]

    with open(self.all, 'w') as f:
        for al in all_lines:
          f.write(al)

    
  def write_to_read(self, author_title):
    with open(self.read, 'a') as f:
        f.write(author_title+'\n')


  def get_all_texts(self):
    all_reads = self.get_texts_list(self.all)
    return [f'{ar[0]}, {ar[1]}, {ar[2]}, {ar[3]}' for ar in all_reads]
