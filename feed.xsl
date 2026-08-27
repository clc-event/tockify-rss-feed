<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/rss/channel">
    <html>
      <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title><xsl:value-of select="title"/></title>
        <style>
          body{font-family:Arial,Helvetica,sans-serif;max-width:800px;margin:0 auto;padding:24px 16px;background:#f7f7f7;color:#222;}
          h1{color:#f26522;margin-bottom:4px;}
          .subtitle{color:#666;margin-top:0;margin-bottom:16px;}
          .subscribe{display:inline-block;margin-bottom:24px;background:#f26522;color:#fff;padding:8px 14px;border-radius:20px;text-decoration:none;font-size:14px;font-weight:600;}
          .item{background:#fff;border-radius:8px;padding:16px 20px;margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,.1);}
          .item h2{margin:0 0 6px;font-size:18px;}
          .item h2 a{color:#222;text-decoration:none;}
          .item h2 a:hover{color:#f26522;}
          .date{color:#888;font-size:13px;margin-bottom:8px;}
          .desc{font-size:14px;line-height:1.55;white-space:pre-wrap;}
        </style>
      </head>
      <body>
        <h1><xsl:value-of select="title"/></h1>
        <p class="subtitle"><xsl:value-of select="description"/></p>
        <a class="subscribe" href="{link}">Voir le calendrier complet</a>
        <xsl:for-each select="item">
          <div class="item">
            <h2><a href="{link}" target="_blank" rel="noopener"><xsl:value-of select="title"/></a></h2>
            <div class="date"><xsl:value-of select="pubDate"/></div>
            <div class="desc"><xsl:value-of select="description"/></div>
          </div>
        </xsl:for-each>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
