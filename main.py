
# 1)  The  generator  function  generatesninitial  randompaintings.
# 2)  The  selector  function  selectsmof  the  initial  randompaintings to mate and produce child paintings.
# 3)  The  crossover  function  takes  two  selected  paintingsand  combines  their  strokes,  half  from  one  and  halffrom  the  other,  to  create  a  child  painting.  It  repeatsthis  process  until  all  of  the  selected  paintings  havebeen mated.
# 4)  Another  selector  function  selectsorandom  membersof the population.
# 5)  The mutation function mutates theseomembers.
# 6)  The simulator then stochastically kills offmpaintingsfrom the population.
# 7)  Go  back  to  step  2  and  repeat  until  a  predeterminednumber of iterations has been met.
# 8)  Render the most fit, according to the fitness function,of the population and output it as the final result.


