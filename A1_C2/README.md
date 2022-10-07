# Semáforo con métodos de sincronización y comunicación

## Contexto de la aplicación

Existen uno o más productores y uno o más consumidores, todos almacenan y extraen productos de una misma bodega. El productor produce productos cada vez que puede, y el consumidor los consume cada vez que lo necesita.

Problema:
coordinar a los productores y consumidores, para que los productores no produzcan más ítems de los que se pueden almacenar en el momento, y los consumidores no adquieran más ítems de los que hay disponibles.
