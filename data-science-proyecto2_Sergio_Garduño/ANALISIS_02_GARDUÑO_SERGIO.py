#!/usr/bin/env python
# coding: utf-8

# ACCESO A GITHUB: https://github.com/SergioGarduno/Proyecto2-Emtech-Institute

# In[51]:


import pandas as pd
import matplotlib.pyplot as plt


# In[52]:


sldb = pd.read_csv('../data/synergy_logistics_database.csv')


# ## 1 Rutas de importación y exportación
# Las rutas se definirán como una combinación de:
# * Origen, destino y medio de transporte

# In[53]:


exportaciones = sldb[sldb['direction']=='Exports']
importaciones = sldb[sldb['direction']=='Imports']
ganancias_totales = sldb['total_value'].sum()


# In[55]:


rutas_exp = exportaciones.groupby(['origin','destination','transport_mode'])
suma_exp = rutas_exp.sum()['total_value']
rutas_exp = rutas_exp['total_value'].describe()
rutas_exp['suma total'] = suma_exp
rutas_exp = rutas_exp.reset_index()


# In[56]:


top_rutas_exp = rutas_exp.sort_values(by = 'count', ascending=False).head(10)
top_rutas_exp


# In[ ]:


rutas_imp = importaciones.groupby(['origin','destination','transport_mode'])
suma_imp = rutas_imp.sum()['total_value']
rutas_imp = rutas_imp['total_value'].describe()
rutas_imp['suma total']=suma_imp
top_rutas_imp = rutas_imp.sort_values(by='count',ascending=False).head(10)
top_rutas_imp


# In[74]:


def ganancias_top(df,top):
    suma_total = df['suma total'].sum()
    top_rutas = df.sort_values(by='suma total', ascending = False).head(top)
    suma_top = top_rutas['suma total'].sum()

    repeticiones = top_rutas['count'].sum()
    porcentaje = (suma_top/suma_total)*1000
    porcentaje = int(porcentaje)/10

    print(f'Las {top} rutas mas demandadas aportan el {porcentaje}% de las ganancias.\nTotal de servicios realizados fue de: {repeticiones} servicios\n')

print("Rutas de exportación")
ganancias_top(rutas_exp,10)
print("Rutas de importación")
ganancias_top(rutas_imp,10)


# Como conclusión para exportaciones, se puede decir que las 10 rutas representan un 6.17% de todas las rutas, pero aprotan un 36.6% de las ganancias. De acuerdo a la regla de pareto (80-20) para realizar una recomendación, el 6.17% tendría que aportar por lo menos 24.68% de las ganancias para que estas 10 rutas sean significativas. Así que si es conveniente realizar una estrategia enfocándose en estas 10 primeras rutas para exportaciones.
# 
# Para el caso de las importaciones, las 10 rutas representan un 19.6% de todas las rutas de importación. De acuerdo a la misma regla, tendrían que aportar mínimo un 78.43% de las ganancias para que fueran representativas y lograr resultados de impacto si se decide enfocar en estas top 10 rutas. Sin embargo, se observa que solo aportan el 52% de las ganancias para importaciones. Lo que nos dice en pocas palabras, es que si se decide enfocar en este 19% de rutas, el reflejo en cuanto a las ganancias será muy pobre. Por lo que significaría mucho esfuerzo por pocas ganancias. Así que para importaciones no es tan recomendable enfocarse en el top 10 rutas, a diferencia de las exportaciones. 

# ## 2. Medio de transporte utilizado

# In[ ]:


def analisis_transporte(direction):
    df = sldb[sldb['direction']==direction]
    df = df.groupby(['transport_mode'])
    df_top = df.count()['total_value']
    df_top = df_top.reset_index()

    ganancias = df['total_value'].sum()
    ganancias = ganancias.reset_index()

    df_top ['ganancias'] = ganancias['total_value']
    t_ganancias = df_top['ganancias'].sum()
    t_rutas = df_top['total_value'].sum()
    df_top['porcentaje_r'] = round((df_top['total_value']/t_rutas)*100,3)
    df_top['porcentaje_g'] = round((df_top['ganancias']/t_ganancias)*100,3)

    df_top = df_top.sort_values('total_value',ascending=False)

    return df_top


# In[ ]:


t_exp = analisis_transporte('Exports')
t_exp


# In[ ]:


t_imp = analisis_transporte('Imports')
t_imp


# Como conclusión se puede decir que se espera que el porcentaje de rutas de algún modo de transporte sea igual al porcentaje de ganancias que generan. Además de este indicador también se podría considerar que el modo de transporte que cuenta con menos rutas como menos ganancias podría ser reducido.
# 
# Para el caso de las exportaciones, sin lugar a duda el modo de transporte más valioso por ruta es el ferroviario. Mientras que el marítimo es el que menos valor aporta por ruta. Para poder llegar a una conclusión más exacta, podrían hacerse futuros análisis históricos para observar como han cambiado las tendencias los últimos años. Porque de ser así, aportaría información igual de importante para tomar una decisión sobre cuál transporte reducir.
# 
# Para el caso de las importaciones, el porcentaje de ganancias que aportan por porcentaje de tipos de rutas es muy parecido. Por lo que este factor parece no ser tan determinante. Por lo que se puede decir que los dos modos de transporte más importantes a considerar para ser reducidos, son tanto por caminos (roads) como los aéreos (air). Ya que estos aportan pocas ganancias y son de por si, las rutas menos utilizadas para importaciones. Sería recomendable realizar un análisis histórico como en el caso pasado, sobre todo para garantizar la calidad del servicio hacia los clientes de Synergy Logistics. 

# ## 3 Valor total de importaciones y exportaciones
# 
# Enfocarse en el 80% de los países que más generan valor de las exportaciones e importaciones

# In[69]:


#Función que devolverá un data frame agrupado por pais de destino u origen, donde se verá un % de ganancias de cada rutas de importacion o exportacion con respecto al valor total.
#Este estará acomodado del que representa un mayor porcentaje del total, a un menor porcentaje. 

def top_valor(df,pais,top):
  imp_exp = df.groupby(pais).sum()
  total = imp_exp['suma total'].sum()
  imp_exp['porcentaje'] =  (imp_exp['suma total'] / total)*100
  imp_exp = imp_exp.sort_values('porcentaje', ascending = False)
  colcumsum = imp_exp.cumsum()['porcentaje']
  imp_exp['porcentaje acum'] = colcumsum
  imp_exp = imp_exp.reset_index()
  top = imp_exp[imp_exp['porcentaje acum'] < top]

  return top


# In[75]:


ex = top_valor(rutas_exp,'origin', 100)
ex


# In[76]:


imp = top_valor(rutas_imp, 'origin', 100)
imp


# Como conclusión se puede mencionar que para el caso de las exportaciones, los primeros 7 países aportan el 75% acumulado de las ganancias. Si bien es muy buen porcentaje, 7 países representa casi la mitad de todos los países exportadores. Lo cual refleja que enfocarse en la mitad de los países, para conseguir un 75% de las ganancias, de acuerdo a la regla de pareto, no sería muy recomendable. Ya que es un gran esfuerzo el tomar la mitad de los países por un resultado no tan alto en cuestión de ganancias.
# 
# Lo mismo sucede para las importaciones. El 76.4% de las ganancias las representan un 41% de los países importadores. Es un gran esfuerzo concentrarse en tantos países, y no resulta del todo redituable. Sin embargo valdría la pena realizar un análisis de mezclas de países importadores y exportadores para saber si pueden hacerse sinergias y aprovechar al doble la oportunidad. Como por ejemplo, enfocarse en China (que aparece en el top de ambas listas) parece ser una idea muy buena. Ya que en total de ganancias, el país de china representa por lo menos un 20% de todas las ganancias, si no es que más. 
# 
# Por lo que sería aconsejable realizar esta mezcla de países para no necesariamente enfocarse en el 80% de las ganancias. Pero si en aquellos casos puntuales, como se puede observa a grandes razgos, China, USA o incluso Japón, que aparecen como grandes importadores y exportadores. 

# ## 4. Conclusión

# Como conclusión se puede decir que cada análisis muestra una perspectiva diferente por la cual se puede obtener información muy valiosa del análisis de la gran cantidad de datos.
# Se puede destacar por ejemplo, que es una buena idea enfocarse en las 10 rutas más concurridas en cuestion de importaciones, que el medio de transporte menos utilizado por Synergy Logistic es por tierra en caso de exportaciones porque aporta poco valor, mientras que para importaciones es menos importante el transporte aereo. Así como también podemos observar que solo 6 países en cuanto a rutas de importación o de exportación representan un valor de 80% de las ganancias totales de SL. Por lo que me parece de gran valor obtener información fácilmente y de una base de datos tan grande. Obtener información representativa y pertinente es vital en cualquier industria y trabajo.
# 
