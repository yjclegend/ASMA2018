function (doc) {
  xmax = 138.78019
  xmin = 138.44213
  ymax = -34.652564
  ymin = -35.34897
  if(doc.coordinates!=null){
    x = doc.coordinates[0]
    y = doc.coordinates[1]
    if( x >= xmin && x <= xmax && y >= ymin && y <= ymax){
      emit(doc._id,doc)
    }
  }
  else{
    if(doc.placename=="Adelaide"){
    emit(doc._id,doc)
    }
  }
}
