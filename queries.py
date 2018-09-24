get_requests_data_query = '''SELECT
  'requestdocument' AS docType,
  r.number AS rNum,
  CONCAT('request_', d.discriminator) AS rDocType,
  CONCAT(d.id, '_', d.realName) AS docName,
  d.uri
FROM request r
  JOIN lot l
    ON l.id = r.lotId
    AND l.active = 1
    AND l.actualId IS NULL
    AND l.archive = 0
  JOIN procedures p
    ON p.id = l.procedureId
    AND p.active = 1
    AND p.actualId IS NULL
    AND p.archive = 0
  JOIN requestDocuments d
    ON d.requestId = r.id
WHERE r.actualId IS NULL
AND r.status != 'request.draft'
AND r.active = 1
AND r.actualId IS NULL
AND r.archive = 0
AND p.registrationNumber = '%(procedure_number)s';'''


get_protocols_data_query = '''SELECT
  'protocol' AS docType,
  CONCAT('protocol_', pr.discriminator) AS pDocType,
  CONCAT(d.id, '_', d.realName) AS docName,
  d.uri
FROM protocol pr
  JOIN lot l
    ON l.id = pr.lotId
    AND l.active = 1
    AND l.actualId IS NULL
    AND l.archive = 0
  JOIN procedures p
    ON p.id = l.procedureId
    AND p.active = 1
    AND p.actualId IS NULL
    AND p.archive = 0
  JOIN protocolDocuments d
    ON d.id = pr.documentId
WHERE p.status != 'protocol.draft'
AND p.registrationNumber = '%(procedure_number)s'
;'''


get_features_data_query = '''SELECT
  'features' AS docType,
  r.number AS rNum,
  CONCAT('features_', rp.code) AS f_code,
  CONCAT(pd.id, '_', pd.realName) AS docName,
  pd.uri
FROM requestPreferences rp
  JOIN request r
    ON r.id = rp.requestId
    AND r.active = 1
    AND r.actualId IS NULL
    AND r.archive = 0
    AND r.status != 'request.draft'
  JOIN lot l
    ON l.id = r.lotId
    AND l.active = 1
    AND l.actualId IS NULL
    AND l.archive = 0
  JOIN procedures p
    ON p.id = l.procedureId
    AND p.active = 1
    AND p.actualId IS NULL
    AND p.archive = 0
  JOIN requestPreferenceDocuments pd
    ON pd.preferenceId = rp.id
 WHERE p.registrationNumber = '%(procedure_number)s'
;'''

get_organisation_id_query = '''SELECT DISTINCT
  r.number,
  r.supplierId
FROM request r
  JOIN lot l
    ON l.id = r.lotId
    AND l.active = 1
    AND l.actualId IS NULL
    AND l.archive = 0
  JOIN procedures p
    ON p.id = l.procedureId
    AND p.active = 1
    AND p.actualId IS NULL
    AND p.archive = 0
WHERE r.active = 1
AND r.actualId IS NULL
AND r.archive = 0
AND r.status != 'request.draft'
AND p.registrationNumber = '%(procedure_number)s'
;'''

get_organisation_data_query = '''SELECT
  'organization_document' AS docType,
  CONCAT('organization_document_', d.documentTypeId) AS pDocType,
  %(request_number)s AS rNum,
  CONCAT(d.id, '_', d.realName) AS docName,
  d.uri
FROM organization.organization o
  JOIN organization.organizationDocuments d
    ON d.organizationId = o.id
WHERE o.id = %(organisation_id)s;'''

get_offers_data_query = '''SELECT
  CONVERT(p.registrationNumber, CHAR) AS 'Процедура',
  l.number AS 'Лот',
  r.id AS 'Номер заявки участника',
  org.fullName AS 'Наименование участника',
  org.inn AS 'ИНН',
  IFNULL(ABS(o.offer), '') AS 'Предложенная цена, руб.',
  IF(o.offer IS NOT NULL, IF(o.offer > 0, 'На понижение v', 'На повышение ^'), '') AS 'Тип ценового предложения',
  IFNULL(o.createDateTime, '') AS 'Дата и время подачи предложения',
  IF(o.valid = 1, '+', '') AS 'C учетом шага цены'
FROM procedures p
  JOIN lot l
    ON l.procedureId = p.id
    AND l.active = 1
    AND l.actualId IS NULL
    AND l.archive = 0
  JOIN request r
    ON r.lotId = l.id
    AND r.active = 1
    AND r.actualId IS NULL
    AND r.archive = 0
    AND r.status != 'request.draft'
  JOIN organization.organization org
    ON org.id = r.supplierId
    AND org.actualId IS NULL
  JOIN tradeOffers o
    ON o.lotId = l.id
    AND o.requestId = r.id
WHERE p.registrationNumber = '%(procedure_number)s'
ORDER BY p.registrationNumber, l.id, o.number DESC
;'''
