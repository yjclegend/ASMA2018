function (doc) {
  xmax = 145.512529
  xmin = 144.593742
  ymax = -37.511274
  ymin = -38.433859
  if(doc.coordinates!=null){
    x = doc.coordinates[0]
    y = doc.coordinates[1]
    if( x >= xmin && x <= xmax && y >= ymin && y <= ymax){
      emit(doc._id,doc)
    }
  }
  else{
    if(doc.placename=="Melbourne"){
      emit(doc._id,doc)
    }
  }
}
