function (doc) {
  xmax = 151.343021
  xmin = 150.520929
  ymax = -33.578141
  ymin = -34.118347
  if(doc.coordinates!=null){
    x = doc.coordinates[0]
    y = doc.coordinates[1]
    if( x >= xmin && x <= xmax && y >= ymin && y <= ymax){
      emit(doc._id,doc)
    }
  }
  else{
    if(doc.placename=="Sydney"){
      emit(doc._id,doc)
    }
  }
}
