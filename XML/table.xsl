<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
  <html>
  <body>
    <h2>My Shop Collection</h2>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>Name</th>
        <th>Image</th>
        <th>Price</th>
      </tr>
      <xsl:for-each select="root/data/product">
      <tr>
        <td width="40%"><xsl:value-of select="name" /></td>
        <td width="20%"><xsl:value-of select="image" /></td>
        <td width="40%"><xsl:value-of select="price" /></td>
      </tr>
      </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>