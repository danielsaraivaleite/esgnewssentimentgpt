<!DOCTYPE html>

<html lang="en" style="height: 100%">
    <head>
        
            <!-- Google tag (gtag.js) -->
            <script async src="https://www.googletagmanager.com/gtag/js?id=G-DHJF51F24N"></script>
            <script>
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());

              gtag('config', 'G-DHJF51F24N');
            </script>
        

        <meta charset="utf-8">
        <title>app.py : /home/esgnewssentiment/app.py : Editor : esgnewssentiment : PythonAnywhere</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="app.py : /home/esgnewssentiment/app.py : Editor : esgnewssentiment : PythonAnywhere">
        <meta name="author" content="PythonAnywhere LLP">
        <meta name="google-site-verification" content="O4UxDrfcHjC44jybs2vajc1GgRkTKCTRgVzeV6I9V14" />


        <!-- Le styles -->
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,300i,400,400i,700,700i" />

        <link rel="stylesheet" href="/static/CACHE/css/output.7fcb6a67fe91.css" type="text/css" media="screen">
        <link rel="stylesheet" href="/static/CACHE/css/output.b9a4961a16f7.css" type="text/css"><link rel="stylesheet" href="/static/CACHE/css/output.f64d871dded0.css" type="text/css" media="screen">

        <!-- Le javascript -->
        <script type="text/javascript">
            var Anywhere = {};
            Anywhere.urls = {};
            Anywhere.csrfToken = "X1aHOG9yKAD8THiV7j8ddyQRWL713DbegXAvUCqyxOh4R3pn7ubSWSyWLc6Lkzkb";
        </script>
        <script src="/static/CACHE/js/output.9912b9c89b96.js"></script>
        

        <script src="/static/CACHE/js/output.a1a307ef0db5.js"></script>
        
    <script type="text/javascript">
      $(document).ready(function() {
        $.extend(Anywhere.urls, {
          file: "/user/esgnewssentiment/files/home/esgnewssentiment/app.py",
          check_hash: "/user/esgnewssentiment/files/home/esgnewssentiment/app.py",
          update_editor_mode_preference: "/user/esgnewssentiment/account/update_editor_mode_preference",
          console_api: "/api/v0/user/esgnewssentiment/consoles/",
        });
        var filename = "/home/esgnewssentiment/app.py";
        var hash = "dfd4190be26f75d3d8fa64d9b2d9cfce";
        var interpreter = "python3.10";

        
            Anywhere.Editor.InitializeAce(ace, Anywhere.urls, filename, hash, interpreter, "pythonanywhere.com");
            $("#id_keybinding_mode_select").val("normal");
            $("#id_keybinding_mode_select").trigger("change");
        
        var consoleVisible = true;
        Anywhere.Editor.splitPanes(consoleVisible);

        Anywhere.WebAppControl.initialize();
        Anywhere2.initializeFileSharingOptions(
          $('#id_file_sharing_options')[0],
          {
            url: "/api/v0/user/esgnewssentiment/files/sharing/",
            csrfToken: "X1aHOG9yKAD8THiV7j8ddyQRWL713DbegXAvUCqyxOh4R3pn7ubSWSyWLc6Lkzkb",
            path: "/home/esgnewssentiment/app.py"
          }
        );

      });
    </script>

        

    </head>

    <body style="height:100%;">
       <div style="min-height: 100%; position: relative;">
        
        
  




  <nav class="navbar navbar-default fullscreen-main-navbar">
    <div class="navbar-header">
      <a class="navbar-brand" href="/">
        <img id="id_logo" src="/static/anywhere/images/PA-logo-snake-only.svg" height="100%" />
      </a>
    </div>

    <div class="extra-nav-content">
      

  <div id="id_editor_toolbar">

    <div class="pull-left">
      <span id="id_breadcrumbs_div"><a class="breadcrumbs_link breadcrumb_entry" href="/user/esgnewssentiment/files/" target="_parent">/</a><a class="breadcrumbs_link breadcrumb_entry" href="/user/esgnewssentiment/files/home" target="_parent">home</a><span class="breadcrumb_entry">/</span><a class="breadcrumbs_link breadcrumb_entry" href="/user/esgnewssentiment/files/home/esgnewssentiment" target="_parent">esgnewssentiment</a><span class="breadcrumb_entry">/</span><wbr><span class="breadcrumb_entry breadcrumb_terminal">app.py</span></span>

      <span>
        <span id="id_unsaved_changes_spacer">
          <span id="id_unsaved_changes" class="pa_hidden muted">(unsaved changes)</span>
        </span>
      </span>
    </div>

    <div id="id_editor_messages" class="pull-left">
      

    </div>

    <div class="pull-right">
      <div id="id_editor_buttons_right" class="form-inline">
        <span id="id_save_error" class="pa_hidden alert alert-danger">Error saving.</span>
        <img src="/static/anywhere/images/spinner-small.gif" class="pa_hidden" id="id_save_spinner" />
        
          <span id="id_keyboard_shortcuts"><a href="#">Keyboard shortcuts:</a></span>
          <select id="id_keybinding_mode_select" class="form-control input-sm">
            <option value="normal">Normal</option>
            <option value="vim">Vim</option>
          </select>
        
        <button id="id_display_sharing_options" class="btn btn-default" data-toggle="modal" data-target="#id_file_sharing_modal" title="Get a URL to share this file">
          <span class="glyphicon glyphicon-paperclip" aria-hidden="true"></span>
          Share
        </button>
        
          <button id="id_save" class="btn btn-success" title="Save (Ctrl + S)">
            <span class="glyphicon glyphicon-floppy-disk" aria-hidden="true"></span>
            Save
          </button>
          <button id="id_save_as" class="btn btn-default" title="Save As">Save as...</button>
        
        
          <button class="btn btn-info run_button" title="Save &amp; Run (Ctrl + R)">
            <span><code>&gt;&gt;&gt;</code></span>
            Run
          </button>
        

        
          
            <form class="reload_web_app" style="display: flex" method="POST" action="/user/esgnewssentiment/webapps/esgnewssentiment.pythonanywhere.com/reload">
              <button class="btn btn-default" type="submit" title="Reload esgnewssentiment.pythonanywhere.com">
                <i class="glyphicon glyphicon-refresh"></i>
              </button>
              <img style="display: none;" class="spinner" src="/static/anywhere/images/spinner-small.gif" />
              <div style="display: none; clear: both;" class="alert alert-danger error_message generic_error">
                There was a problem. If this keeps happening, please <a href="" class="feedback_link">send us feedback</a>.
              </div>
              <div style="display: none; clear: both;" class="alert alert-danger error_message slow_startup_error">
                Your webapp took a long time to reload. It probably reloaded, but we were unable to check it.
              </div>
              <div style="display: none; clear: both;" class="alert alert-danger error_message virtualenv_error">
                There is a problem with your virtualenv setup. Look at the <b>virtualenv</b> section on the web app tab for details.
              </div>
              <div style="display: none; clear: both;" class="alert alert-danger error_message cname_error">
                There is a problem with your DNS configuration. Take a look at the <b>DNS setup</b> section on the web app tab for details.
              </div>
            </form>
          
        
      </div>
    </div>

  </div>


    </div>

    <div class="dropdown fullscreen-hamburger fullscreen-mini-nav">
      <button type="button" class="navbar-toggle" data-toggle="dropdown"  role="button" aria-haspopup="true" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <ul class="dropdown-menu pull-right">
        
  <li class=""><a id="id_dashboard_link" href="/user/esgnewssentiment/">Dashboard</a></li>
  <li class=""><a id="id_consoles_link" href="/user/esgnewssentiment/consoles/">Consoles</a></li>
  <li class=""><a id="id_files_link" href="/user/esgnewssentiment/files/home/esgnewssentiment">Files</a></li>
  <li class=""><a id="id_web_app_link" href="/user/esgnewssentiment/webapps/">Web</a></li>
  <li class=""><a id="id_tasks_link" href="/user/esgnewssentiment/tasks_tab/">Tasks</a></li>
  <li class=""><a id="id_databases_link" href="/user/esgnewssentiment/databases/">Databases</a></li>


        
<li class=""><a href="" target="_parent" class="feedback_link">Send feedback</a></li>


<li class=""><a href="/forums/" target="_parent" class="forums_link">Forums</a></li>
<li class=""><a href="https://help.pythonanywhere.com/" target="_parent" class="help_link">Help</a></li>
<li class=""><a href="https://blog.pythonanywhere.com/" target="_parent" class="blog_link">Blog</a></li>

  
  <li class=""><a href="/user/esgnewssentiment/account/" target="_parent" class="account_link">Account</a></li>
  <li class="">
    <form action="/logout/" method="POST" target="_parent">
      <input type="hidden" name="csrfmiddlewaretoken" value="X1aHOG9yKAD8THiV7j8ddyQRWL713DbegXAvUCqyxOh4R3pn7ubSWSyWLc6Lkzkb">
      <button type="submit" class="btn-link logout_link">Log out</button>
    </form>
  </li>


      </ul>
    </div>

  </nav>



        
    


        
  <div>
    <div id="id_ide_split_panes">

      
        <div id="id_editor">&#39;&#39;&#39;
Aplicativo WEB em FLASK para apresentar a analise de sentimento das noticias
Autor: Daniel Saraiva Leite - 2023
Projeto Análise de sentimentos sobre notícias do tema ESG
Trabalho de conclusão de curso - MBA Digital Business USP Esalq
&#39;&#39;&#39;


from flask import Flask, render_template, request
import os
import pandas as pd
import datetime as dt
from analise_sentimento_modelo import gera_curva_polaridade_media
from noticias_graficos import *
from noticias_wordcloud import plotar_word_cloud

base_noticias_saida = &#39;datasets/sentimento_base_noticias_short.xlsx&#39;
df = pd.read_excel(base_noticias_saida)

app = Flask(__name__)

@app.route(&#39;/&#39;, methods=[&#39;GET&#39;, &#39;POST&#39;])
def index():
    &#39;&#39;&#39;
    Página principal do app que mostra o sentimento das noticias
    O resultado mostrado da analise ja foi previamente gerado nas Jupyter notebooks do projeto
    &#39;&#39;&#39;
    # carrega lista de empresas
    nomes_empresas = list(df.sort_values(by=&#39;empresa&#39;)[&#39;empresa&#39;].drop_duplicates())

    # processa a busca
    if request.method == &#39;POST&#39;:
        empresa = request.form.get(&#39;nomes&#39;)

        dfEmpresa = df[df[&#39;empresa&#39;] == empresa]

        # adiciona o formato de exibicao
        dfEmpresa[&#39;formato&#39;] = dfEmpresa[&#39;polaridade&#39;].apply(formato_tabela)

        # converte a tabela pra dicionario permitindo a exibicao
        tabela_dados_pos = dfEmpresa[dfEmpresa.polaridade&gt;0.05].to_dict(orient=&#39;records&#39;)
        tabela_dados_neg = dfEmpresa[dfEmpresa.polaridade&lt;-0.05].to_dict(orient=&#39;records&#39;)

        # ultima noticia
        ultima_data = dfEmpresa[&#39;data_publicacao&#39;].max().strftime(&#39;%d/%m/%Y&#39;)

        calibragem_alfa = [0.07, 0.075, 0.1, 0.15]

        # plota grafico polaridade media
        lista_dfs_polaridade = [gera_curva_polaridade_media(df, empresa, &#39;ESG&#39;, alfa=calibragem_alfa[0]),
                                gera_curva_polaridade_media(df, empresa, &#39;E&#39;, alfa=calibragem_alfa[1]),
                                gera_curva_polaridade_media(df, empresa, &#39;S&#39;, alfa=calibragem_alfa[2]),
                                gera_curva_polaridade_media(df, empresa, &#39;G&#39;, alfa=calibragem_alfa[3])]
        graph_path = (os.path.join(&#39;static&#39;, &#39;images&#39;, &#39;grafico_polaridade.png&#39;))
        plota_polaridade_media_sintetico(df, empresa, arquivo=graph_path, lista_dfs_polaridade=lista_dfs_polaridade)

        # plota os gauges
        plotar_gauge_polaridade(df, empresa=empresa, dimensao=&#39;ESG&#39;, df_pol=lista_dfs_polaridade[0], arquivo=os.path.join(&#39;static&#39;, &#39;images&#39;, &#39;gauge_esg.png&#39;))
        plotar_gauge_polaridade(df, empresa=empresa, dimensao=&#39;E&#39;, df_pol=lista_dfs_polaridade[1], arquivo=os.path.join(&#39;static&#39;, &#39;images&#39;, &#39;gauge_e.png&#39;))
        plotar_gauge_polaridade(df, empresa=empresa, dimensao=&#39;S&#39;, df_pol=lista_dfs_polaridade[2], arquivo=os.path.join(&#39;static&#39;, &#39;images&#39;, &#39;gauge_s.png&#39;))
        plotar_gauge_polaridade(df, empresa=empresa, dimensao=&#39;G&#39;, df_pol=lista_dfs_polaridade[3], arquivo=os.path.join(&#39;static&#39;, &#39;images&#39;, &#39;gauge_g.png&#39;))

        # base de dados
        plotar_descricao_base(dfEmpresa, plotar_histograma=True, arquivo=r&#39;static/images/grafico_base_dados.png&#39;)

        # timeline
        plota_timeline_polaridade(dfEmpresa, +1, numero_noticias=2, empresa=empresa, imprime=False, arquivo=os.path.join(&#39;static&#39;, &#39;images&#39;, &#39;grafico_timeline_pos.png&#39;) )
        plota_timeline_polaridade(dfEmpresa, -1, numero_noticias=2, empresa=empresa, imprime=False, arquivo=os.path.join(&#39;static&#39;, &#39;images&#39;, &#39;grafico_timeline_neg.png&#39;) )

        # wordclouds
        plotar_word_cloud(dfEmpresa, empresa=empresa, dimensao=&#39;E&#39;, arquivo=os.path.join(&#39;static&#39;, &#39;images&#39;, &#39;wordcloud_E.png&#39;), coluna_texto=&#39;gpt_resumo&#39;)
        plotar_word_cloud(dfEmpresa, empresa=empresa, dimensao=&#39;S&#39;, arquivo=os.path.join(&#39;static&#39;, &#39;images&#39;, &#39;wordcloud_S.png&#39;), coluna_texto=&#39;gpt_resumo&#39;)
        plotar_word_cloud(dfEmpresa, empresa=empresa, dimensao=&#39;G&#39;, arquivo=os.path.join(&#39;static&#39;, &#39;images&#39;, &#39;wordcloud_G.png&#39;), coluna_texto=&#39;gpt_resumo&#39;)

        return render_template(&#39;index.html&#39;, nomes=nomes_empresas, tabela_pos=tabela_dados_pos,
                                tabela_neg=tabela_dados_neg, empresa_selecionada=empresa, ultima_data=ultima_data)

    return render_template(&#39;index.html&#39;, nomes=nomes_empresas)


def formato_tabela(n):
    &#39;&#39;&#39;
    Define o Formato da tabela (heatmap) de acordo com polaridade
    &#39;&#39;&#39;
    cor_fundo = &#39;bg-success p-2&#39;
    text = &#39;text-dark&#39;
    opacidade = &#39;bg-opacity-10&#39;
    if (n &lt; 0):
        cor_fundo = &#39;bg-danger p-2&#39;
        n = -1 * n

    if n &gt;= 0.75:
        opacidade = &#39;&#39;
        text = &#39;text-white&#39;
    elif n &gt;= 0.5 and n&lt;0.75:
        text = &#39;text-white&#39;
        opacidade = &#39;bg-opacity-75&#39;
    elif n &gt;= 0.25 and n&lt;0.5:
        opacidade = &#39;bg-opacity-50&#39;
    elif n &gt;= 0.10 and n&lt;0.25:
        opacidade = &#39;bg-opacity-25&#39;
    return cor_fundo + &#39; &#39; + text + &#39; &#39; + opacidade



if __name__ == &#39;__main__&#39;:
    app.run(debug=True)
</div>
      

      <div id="id_ide_console">
        
          <div id="id_ide_console_pane_buttons">
            <center>
              
                <button class="btn btn-large btn-info run_button" title="Save &amp; Run (Ctrl + R)">&gt;&gt;&gt; Run this file</button>
                <button class="btn btn-large btn-info bash_console_here" title="Start a Bash console in this folder">$ Bash console here</button>
              
            </center>
          </div>
          <iframe style="display: none" id="id_console" name="console" class="soft_keyboard_sensitive">
          </iframe>
          <div style="display: none;" class="console_limit_reached">
            <div class="container">
    <div class="row">
        <div class="col-md-5 col-md-offset-3 well">
            <h1>Console limit reached :-/</h1>

            <p>
            With your current PythonAnywhere account you can have up to
            999 consoles.  You can
            have more if you
            <a href="/user/esgnewssentiment/account/">upgrade your account</a>!

            <p>
            Alternatively, if you don't feel like paying us more money, you
            can <a href="/user/esgnewssentiment/consoles/">kill some consoles on your Consoles page</a>.
        </div>
    </div>
</div>


          </div>
        
      </div>

    </div>

    <div id="id_go_to_line_dialog" class="pa_hidden">
      <p class="form-inline">Line number: <input id="id_go_to_line_dialog_input" /></p>
      <div class="dialog_buttons">
        <button class="btn btn-default" id="id_go_to_line_dialog_ok_button">Go</button>
        <button class="btn btn-default" id="id_go_to_line_dialog_close_button">Close</button>
      </div>
    </div>

    <div id="id_file_changed_on_disk" class="pa_hidden">
      <p>Are you sure you want to save it?  Alternatively, you could re-open it in a new tab to check differences</p>
      <div class="dialog_buttons">
        <button id="id_force_save" class="btn btn-danger">Force Save</button>
        <button id="id_cancel_save" class="btn btn-default">Cancel</button>
      </div>
    </div>

    <div id="id_save_as_dialog" class="pa_hidden">
      <form class="form-inline">
        <div class="form-group">
          <label for="id_save_as_path">Please enter a path:</label>
          <input id="id_save_as_path" class="form-control" style="width: 100%;" />
        </div>
        <img id="id_save_as_spinner" class="spinner pa_hidden" src="/static/anywhere/images/spinner-small.gif" />
        <p>
          <span id="id_save_as_error" class="error_message"></span>
        </p>
        <div class="dialog_buttons">
          <button id="id_save_as_ok" type="submit" class="btn btn-primary">Save</button>
          <button id="id_save_as_cancel" type="button" class="btn btn-default">Cancel</button>
        </div>
      </form>
    </div>

    <div class="modal fade" id="id_file_sharing_modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <h4 class="modal-title" id="myModalLabel">File Sharing options</h4>
          </div>
          <div class="modal-body">
            <div id="id_file_sharing_options"></div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>

  </div>


        
      </div>

        


        <div id="id_feedback_dialog" title="Help us improve" style="display:none">
    <div id="id_feedback_dialog_blurb_big" class="dialog_blurb_big">
        It's always a pleasure to hear from you!
    </div>
    <div id="id_feedback_dialog_blurb_small">
        Ask us a question, or tell us what you love or hate about PythonAnywhere.<br/>
        We'll get back to you over email ASAP.
    </div>
    <textarea id="id_feedback_dialog_text" rows="6"></textarea>
    <input id="id_feedback_dialog_email_address" type="text" placeholder="Email address (optional - only necessary if you would like us to contact you)"/>
    
    <div id="id_feedback_dialog_error" style="display: none">
        Sorry, there was an error connecting to the server. <br/>Please try again in a few moments...
    </div>
    <div id="id_feedback_dialog_rate_limit_error" style="display: none">
        Sorry, we have had to rate-limit your feedback sending.<br/>Please try again in a few moments...
    </div>
    <div id="id_feedback_dialog_success" style="display: none">
        Thanks for the feedback! Our tireless devs will get back to you soon.
    </div>
    <div class="dialog_buttons">
        <img id="id_feedback_dialog_spinner" src="/static/anywhere/images/spinner-small.gif" />
        <button class="btn btn-primary" id="id_feedback_dialog_ok_button">OK</button>
        <button class="btn btn-default" id="id_feedback_dialog_cancel_button">Cancel</button>
    </div>
    <div id="id_feedback_dialog_only_close_button" style="display: none">
        <button class="btn btn-primary" id="id_feedback_dialog_close_button">Close</button>
    </div>
</div>


        
        <!-- preload font awesome fonts to avoid glitch when switching icons -->
        <div style="width: 0; height: 0; overflow: hidden"><i class="fa fa-square-o fa-3x" ></i></div>
    </body>
</html>
