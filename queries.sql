SELECT ID from Surfaces where Path like '%Light%';

SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%Light%';

SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%cap%';

SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%Heliostat%';

SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%aux%';

SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%abs%';


SELECT abs*100.0/mirrors as efficiency FROM 
(SELECT count() as abs from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%abs%'),
(SELECT count() as mirrors from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%Heliostat%');
