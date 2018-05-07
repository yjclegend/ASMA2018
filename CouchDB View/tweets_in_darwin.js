function (doc) {
  xmax = 131.0515
  xmin = 130.815117
  ymax = -12.33006
  ymin = -12.521742
  if(doc.coordinates!=null){
    x = doc.coordinates[0]
    y = doc.coordinates[1]
    if( x >= xmin && x <= xmax && y >= ymin && y <= ymax){
      emit(doc._id,doc)
    }
  }
  else{
    if(doc.placename=="Darwin"){
      emit(doc._id,doc)
    }
  }
}
