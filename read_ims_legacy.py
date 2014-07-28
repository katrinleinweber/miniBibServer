def read_ims_legacy(name):
    data = {}
    dls = []
    #should read in .tex file
    infile = open(name + ".tex")
    instring = infile.read()
    ##instring = instring.replace(':description','    :citation')   ##  to be deprecated soon
    instring = unicode(instring,'utf-8')
    meta = {}
    
    metatxt = instring.split('::')[1]
    meta['record_txt'] =  '::' + metatxt.strip() + '\n\n'
    meta['bibtype'],rest= metatxt.split(None,1)
    meta['id'],rest= rest.split(None,1)
    rest = '\n' + rest.strip()
    secs = rest.split('\n:')[1:]
    for sec in secs:
        k,v = sec.split(None,1)
        meta[k] = v
    data['metadata'] = meta
    for x in instring.split('::person')[1:]:
        x = x.split('\n::')[0]
        d = {}
        d['record_txt'] = '::person ' + x.strip() + '\n'
        lines = d['record_txt'].split('\n')
        lines = [line for line in lines if not line.find('Email') >= 0 ]
        pubrecord = '\n'.join(lines) + '\n'
        d['public_record_txt'] =  break_txt(pubrecord,80)
        secs = x.split('\n:')
        toplines = secs[0].strip()
        d['id'], toplines  = toplines.split(None,1)
        try: name,toplines = toplines.split('\n',1)
        except: 
            name = toplines
            toplines = ''
        d['complete_name'] = name
        #d['link_lines'] = toplines
        d['link_ls'] = lines2link_ls(toplines)
        for sec in secs[1:]:
            words = sec.split()
            key = words[0]
            if len(words) > 1:
                val = sec.split(None,1)[1]   ## keep newlines
            else: val = ''
            if d.has_key(key): d[key] += [val]
            else: d[key] = [val]
        d['Honor'] = [ read_honor(x) for x in d.get('Honor',[]) ]
        d['Degree'] = [ read_degree(x) for x in d.get('Degree',[]) ]
        d['Education'] = [ read_education(x) for x in d.get('Education',[]) ]
        d['Service'] = [ read_service(x) for x in d.get('Service',[]) ]
        d['Position'] = [ read_position(x) for x in d.get('Position',[]) ]
        d['Member'] = [ read_member(x) for x in d.get('Member',[]) ]
        d['Image'] = [ read_image(x) for x in d.get('Image',[]) ]
        d['Homepage'] = [ read_homepage(x) for x in d.get('Homepage',[]) ]
        for k in bio_cat_order:
            #d['Biography'] = [ read_bio(x) for x in d.get('Biography',[]) ]
            d[k] = [ read_bio(x) for x in d.get(k,[]) ]
        dls += [d]
    links_txt = instring.split('::links',1)[1].split('\n::')[0]
    data['link_ls'] = links_txt2ls(links_txt)
    data['records'] = dls
    books = instring.split('::book')[1:]
    book_dict = {}
    for b in books:
        b = 'book' + b
        d = read_book(b)
        del d['top_line']
        book_dict[ d['id'] ] = d
    data['books'] = book_dict
    links_txt = instring.split('::links',1)[1].split('\n::')[0]
    data['link_ls'] = links_txt2ls(links_txt)
    return data