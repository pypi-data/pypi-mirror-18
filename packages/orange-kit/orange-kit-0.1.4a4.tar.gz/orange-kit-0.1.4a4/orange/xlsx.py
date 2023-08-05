# 项目：Excel写入模块封装
# 模块：xlsxwriter的封装
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-10-12 08:24

from orange import *
from xlsxwriter import *
from xlsxwriter.format import Format
from xlsxwriter.worksheet import *

Pattern=R/r'([A-Z]{1,2})(\d*)([:_]([A-Z]{1,2})(\d*))?'
Row=R/r'(\{([+-]?\d+)\})'

DefaultFormat=(('currency',{'num_format':'#,##0.00'}),
                ('rate',{'num_format':'0.0000%'}),
                ('title',{'font_name':'黑体','font_size':16,
                          'align':'center'}),
                ('h2',{'font_name':'黑体','font_size':12,
                          'align':'center'}),
                ('mh2',{'font_name':'黑体','font_size':12,
                          'align':'center','valign':'vcenter'}),
                ('percent',{'num_format':'0.00%'}),
                ('date',{'num_format':'yyyy-mm-dd'}),
                ('time',{'num_format':'hh:mm:ss'}),
                ('number',{'num_format':'#,##0'}),
                ('datetime',{'num_format':'yyyy-mm-dd hh:mm:ss'}),
                ('timestamp',{'num_format':'yyyy-mm-dd hh:mm:ss.0'}))

class Book(Workbook):
    ''' 对Xlsxwriter模块进一步进行封装'''
    def __init__(self,filename=None,**kw):
        if isinstance(filename,str):
            filename=str(Path(filename))
        super().__init__(filename,**kw)
        self._worksheet=None    # 设置当前的工作表为空
        self._worksheets={}     # 设置当前的工作表清单为空
        self._formats={}
        for name,val in DefaultFormat:
            self.add_format(val,name)

    def add_format(self,properties,name=None):
        _format=super().add_format(properties)
        if name:
            self._formats[name]=_format
            _format.name=name
            _format.properties=properties
        return _format
                
    def set_columns(self,*columns,width=None,cell_format=None,options=None):
        ''' 设置当前工作表的列属性，允许同时设置多个，使用方法如下：
        book.set_columns('A:C','E:D','G:H',width=12)
        '''
        options=options or {}
        for column in columns:
            self.worksheet.set_column(column,width,cell_format,options)

    def newline(self):
        '''换行'''
        return self+1
        
    @property
    def worksheet(self):
        '''当前工作表'''
        return self._worksheet

    @worksheet.setter
    def worksheet(self,name):
        '''切换当前工作表'''
        worksheet=self._worksheets.get(name,None)
        if not worksheet:
            worksheet=self.add_worksheet(name)
            worksheet.row=1
            self._worksheets[name]=worksheet
        self._worksheet=worksheet
        
    def write(self,range,value,format=None):
        '''写入单元格'''
        if isinstance(format,str):  # 格式代码检查
            format=self._formats.get(format)
        if ':' in range and not isinstance(value,(dict,tuple,list)):
            self.worksheet.merge_range(range,value,format)
        if ':' not in range:
            if isinstance(value,(list,tuple)):
                self.worksheet.write_row(range,value,format)
            else:
                if isinstance(value,str) and value.startswith('='):
                    value=Row/value%self._convert   # 使用正则表达式替换
                self.worksheet.write(range,value,format)

    def _convert(self,match):
        return str(int(match.groups()[1])+self.row)

    def __add__(self,val):
        '''向前移动当前行'''
        self.worksheet.row+=val
        return self
    
    def __sub__(self,val):
        '''向后移动当前行'''
        self.worksheet.row-=val
        return self

    @property
    def row(self):
        '''获取当前工作表的行'''
        return self.worksheet.row

    @row.setter
    def row(self,currow):
        '''设置当前工作表的行'''
        self.worksheet.row=currow
    
    def __setitem__(self,name,val):
        '''向指定行写入数据'''
        match=Pattern.fullmatch(name)
        if match:
            r=list(match.groups())
            if not r[1]:
                r[1]=str(self.row)
            rg=''.join(r[:2])
            if r[3]:
                if not r[4]:
                    r[4]=str(self.row)
                rg='%s:%s%s'%(rg,r[3],r[4])
            if not isinstance(val,tuple):
                val=(val,)
            self.write(rg,*val)
        else:
            raise Exception('单元格格式不正确')

    def __setattr__(self,name,val):
        '''向指定行写入数据'''
        try:
            self[name]=val
        except:
            super().__setattr__(name,val)

    def iter_rows(self,*datas,step=1):
        '''按行写入数据'''
        for d in zip(*datas):
            yield d
            self+=step

    @property
    def table(self):
        return self.worksheet.table

    @convert_range_args
    def set_border(self, first_row, first_col, last_row, last_col,
                  left=None,right=None,bottom=None,top=None,border=2,
                  inner=1):
        self.worksheet._check_dimensions(first_row,first_col)
        self.worksheet._check_dimensions(last_row,last_col)
        if border:
            left=left or border
            right=right or border
            bottom=bottom or border
            top=top or border
        table=self.table        
        default_format={"left":inner,"right":inner,"top":inner,
                               "bottom":inner}
        def _replace(r,c,**kw):
            row=table[r]
            cell=row.get(c,cell_blank_tuple(None))
            fmt=cell.format
            kw['top']=top if r==first_row else inner
            kw['bottom']=bottom if r==last_row else inner
            kw['left']=left if c==first_col else inner
            kw['right']=right if c==last_col else inner
            name=''.join([str(kw[name]) for name in \
                          'left top right bottom'.split()])
            if fmt and hasattr(fmt,'name'):
                name=name+'-'+fmt.name
            if not name in self._formats:
                if fmt and hasattr(fmt,'properties'):
                    a=fmt.properties.copy()
                    a.update(kw)
                else:
                    a=kw
                new_fmt=self.add_format(a,name)
            else:
                new_fmt=self._formats.get(name)
            row[c]=cell._replace(format=new_fmt)
        [_replace(r,c)for r in range(first_row,last_row+1)\
         for c in range(first_col,last_col+1)]
        
if __name__=='__main__':
    with Book('~/test.xlsx') as book:
        book.worksheet='test1'
        book.B2=["test","2","3","4"],'title'
        book.worksheet='test2'
        book.row=3
        for a,b in book.iter_rows(range(1,11),range(1,11)):
            book.A=a,'number'
            book.B=b/100,'percent'
        book.set_border('B3:D4')

        book.set_border('B15')
        book.set_border('A17:C18',left=6)
        book.set_border('A20:C20')
        book.set_border('D23:A22')

