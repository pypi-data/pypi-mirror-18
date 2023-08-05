def data(data,columns=''):
    
    """
      Data processor for desc_table() function.
      
      You can call it separately as well and in 
      return get a non-prettyfied summary table. 
      
      Unless columns are defined, the three first 
      columns are chosen by default. 
      
      SYNTAX EXAMPLE: 
      
      df['quality_score','influence_score','reach_score']
    
    """
    import pandas as pd
    
    if data.shape[1] != 3:
        if len(columns) !=3:
            if data.shape[1] > 3:
                
                print "showing first three columns because no columns were specific / data had more than 3 columns"
                data = pd.DataFrame(data[data.columns[0:3]])
    
    if data.shape[1] < 3:
        
        print "You need at least 3 columns of data for this table"
        quit()
        
    if len(columns) == 3:
            data = data[columns]
            
    desc = pd.DataFrame({'sum' : data.sum().astype('int'),
                         'median' : data.median(),
                         'mean' : data.mean(),
                         'std' : data.std()})
    desc = desc.round(decimals=2)      
    
    return desc

def table(data,title="Descriptive Stats",table_title=""):
    
    """
      Takes in 3 features/columns of data, and
      returns a prettified publication quality 
      descriptive stats summary table. 
      
      The default column setting is for scores. 

      data = a pandas DataFrame
      columns = the columns inside [] and comma (,) separated 
                
                OPTIONS: 'score', 'user', 'polarity' or create
                one yourself using syntax like so: 
                
                df['quality_score','influence_score','reach_score']
                
    """

    from IPython.core.display import display, HTML
    display(HTML("<style type=\"text/css\"> .tg {border-collapse:collapse;border-spacing:0;border:none;} .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;} .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;} .tg .tg-ejgj{font-family:Verdana, Geneva, sans-serif !important;;vertical-align:top} .tg .tg-anay{font-family:Verdana, Geneva, sans-serif !important;;text-align:right;vertical-align:top} .tg .tg-jua3{font-weight:bold;font-family:Verdana, Geneva, sans-serif !important;;text-align:right;vertical-align:top} h5{font-family:Verdana;} h4{font-family:Verdana;} hr{height: 3px; background-color: #333;} .hr2{height: 1px; background-color: #333;} </style> <table class=\"tg\" style=\"undefined;table-layout: fixed; width: 500px; border-style: hidden; border-collapse: collapse;\"> <colgroup> <col style=\"width: 150px\"> <col style=\"width: 120px\"> <col style=\"width: 120px\"> <col style=\"width: 120px\"> <col style=\"width: 120px\"> </colgroup> <h5>" + str(table_title) + "</h5> <h4><i>" + str(title) + "</i></h4> <hr align=\"left\", width=\"630\"> <tr> <th class=\"tg-ejgj\"></th> <th class=\"tg-anay\">median</th> <th class=\"tg-anay\">mean</th> <th class=\"tg-anay\">std</th> <th class=\"tg-anay\">total</th> </tr> <tr> <td class=\"tg-ejgj\">" + data.index[0] + "</td> <td class=\"tg-jua3\">" + str(data['median'][0]) + "</td> <td class=\"tg-jua3\">" + str(data['mean'][0]) + "</td> <td class=\"tg-jua3\">" + str(data['std'][0]) + "</td> <td class=\"tg-jua3\">" + str(data['sum'][0]) + "</td> </tr> <tr> <td class=\"tg-ejgj\">" + data.index[1] + "</td> <td class=\"tg-jua3\">" + str(data['median'][1]) + "</td> <td class=\"tg-jua3\">" + str(data['mean'][1]) + "</td> <td class=\"tg-jua3\">" + str(data['std'][1]) + "</td> <td class=\"tg-jua3\">" + str(data['sum'][1]) + "</td> </tr> <tr> <td class=\"tg-ejgj\">" + data.index[2] + "</td> <td class=\"tg-jua3\">" + str(data['median'][2]) + "</td> <td class=\"tg-jua3\">" + str(data['mean'][2]) + "</td> <td class=\"tg-jua3\">" + str(data['std'][2]) + "</td> <td class=\"tg-jua3\">" + str(data['sum'][2]) + "</td> </tr> </table> <hr align=\"left\", width=\"630\">"))

def toggle():

    from IPython.display import HTML
    
    tog = HTML('''<script>
    code_show=true; 
    function code_toggle() {
     if (code_show){
     $('div.input').hide();
     } else {
     $('div.input').show();
     }
     code_show = !code_show
    } 
    $( document ).ready(code_toggle);
    </script>
    The raw code for this IPython notebook is by default hidden for easier reading.
    To toggle on/off the raw code, click <a href="javascript:code_toggle()">here</a>.''')
    return tog

def warnings():
    import warnings
    warnings.filterwarnings('ignore')