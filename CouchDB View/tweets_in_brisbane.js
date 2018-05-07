function (doc) {
  xmax = 153.31787
  xmin = 152.668523
  ymax = -26.996845
  ymin = -27.767441
  if(doc.coordinates!=null){
    x = doc.coordinates[0]
    y = doc.coordinates[1]
    if( x >= xmin && x <= xmax && y >= ymin && y <= ymax){
      emit(doc._id,doc)
    }
  }
  else{
    if(doc.placename=='Brisbane'){
    emit(doc._id,doc);
    }
  }
}
