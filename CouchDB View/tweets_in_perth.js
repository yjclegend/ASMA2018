function (doc) {
  xmax = 115.877911
  xmin = 115.827166
  ymax = -31.936494
  ymin = -31.97289
  if(doc.coordinates!=null){
    x = doc.coordinates[0]
    y = doc.coordinates[1]
    if( x >= xmin && x <= xmax && y >= ymin && y <= ymax){
      emit(doc._id,doc)
    }
  }
  else{
    if(doc.placename=="Perth"){
      emit(doc._id,doc)
    }
  }
}
