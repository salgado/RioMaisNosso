#!/usr/bin/env python
# -*- coding: utf-8 -*-

# exemplo de codigo do trecho do site
# http://www.riomaisnosso.com/reversiveis/

import sys
import requests
import datetime, xmlrpclib

class Reversiveis:
    def __init__(self):
        print "Reversiveis"

    def publica(self):
        my_config = {'verbose': sys.stderr}

        strToken= "seu token para acesso ao web server"

        request_token_url = "http://api.riodatamine.com.br/rest/request-token?" + strToken
        
        r = requests.get(request_token_url,prefetch=True)

        access_token = r.headers['x-access-token']

        headers = { 'Authorization' : access_token}

        url2 = 'http://api.riodatamine.com.br/rest/transito/vias/reversiveis?format=json'
        r = requests.get(url2, headers=headers, config=my_config)

        print r.content

        transito = r.content

        #print transito

        import json

        transito = json.loads(transito)

        #print transito
        x=0
        twit = ""
        linha=""
        novalinha=""
        trechoPonte = {}
        rampas = {}
        bairros = {}

        # acesso aos campos retornados do json
        for xitems in transito["results"]:
            nome = xitems['name']
            descricao = xitems['description']['text']
            if 'description' in xitems:
                x=x+1

                linha=""
                linha = linha + "<tr>"
                linha = linha + "<td>"
                linha = linha + nome
                linha = linha + "</td>"
                linha = linha + "<td>"
                linha = linha + descricao
                linha = linha + "</td>"
                linha = linha + "</tr>"
                novalinha = novalinha + linha

        cabecalho = "<table class='table table-bordered table-striped'>"
        cabecalho = cabecalho + "    <thead>"
        cabecalho = cabecalho + "      <tr>"
        cabecalho = cabecalho + "        <th>Localiza&ccedil;&atilde;o</th>"
        cabecalho = cabecalho + "        <th>Descri&ccedil;&atilde;o</th>"
        cabecalho = cabecalho + "      </tr>"
        cabecalho = cabecalho + "    </thead>"
        cabecalho = cabecalho + "    <tbody>"

        cabTrechoPonte = ''

        footer = "</tbody>"
        footer = footer + "</table>"

        today = datetime.datetime.today()
        today = today + datetime.timedelta(hours=4)
        s = today.strftime("%d-%m-%Y %H:%M")
        
        content = cabTrechoPonte + "<small>(" + s + ")</small>" + cabecalho + novalinha + footer

        #print content

        wp_url = "sua url com protocolo xmlrpc"
        wp_username = "usuario"
        wp_password = "senha"
        wp_blogid = "id da pagina"

        status_draft = 0
        status_published = 1

        server = xmlrpclib.ServerProxy(wp_url)

        today = datetime.datetime.today()
        today = today + datetime.timedelta(hours=0)

        s = today.strftime("%Y-%m-%d %H:%M")

        title = "<h1>Reversíveis</h1>"

        date_created = xmlrpclib.DateTime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M"))
        print date_created

        categories = ["transito"]
        tags = ["reversíveis rio de janeiro"]
        data = {'title': title, 'description': content, 'dateCreated': date_created, 'categories': categories, 'mt_keywords': tags}

        post_id = server.metaWeblog.editPost(wp_blogid, wp_username, wp_password, data, status_published)
