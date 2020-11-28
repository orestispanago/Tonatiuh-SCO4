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

-- 5-6% slower
SELECT 
(SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%Light%') AS sun,
(SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%Heliostat%' AND Photons.side=0) 
AS reflectors_back,
(SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%Heliostat%' AND Photons.side=1) 
AS reflectors_front,
(SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%abs%' AND Photons.side=0) 
AS absorber_bottom,
(SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%abs%' AND Photons.side=1) 
AS absorber_top,
(SELECT * FROM wphoton) as wphoton; 

-- Watts
SELECT 
(SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%Light%')*
(SELECT power from wphoton) 
AS sun,
(SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%Heliostat%' AND Photons.side=0)*
(SELECT power from wphoton) 
AS reflectors_back,
(SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%Heliostat%' AND Photons.side=1)*
(SELECT power from wphoton) 
AS reflectors_front,
(SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%abs%' AND Photons.side=0)*
(SELECT power from wphoton) 
AS absorber_bottom,
(SELECT count() from Surfaces,Photons
where Photons.surfaceID=Surfaces.id 
AND Surfaces.Path like '%abs%' AND Photons.side=1)*
(SELECT power from wphoton) 
AS absorber_top;


