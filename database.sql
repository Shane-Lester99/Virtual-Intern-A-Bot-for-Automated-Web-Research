CREATE TABLE  User (
	Email varchar(255) NOT NULL,
	Password TEXT NOT NULL,
	authKey TEXT NOT NULL,
	PRIMARY KEY (Email)
);

CREATE TABLE Query (
	QueryID INT NOT NULL AUTO_INCREMENT,
	SearchString TEXT NOT NULL,
	PRIMARY KEY (QueryID)
);

CREATE TABLE ReferenceLink (
	ReferenceLinkID INT NOT NULL AUTO_INCREMENT,
	Url TEXT NOT NULL,
	PRIMARY KEY (ReferenceLinkID)
);

CREATE TABLE HitLink (
	HitLinkID INT NOT NULL AUTO_INCREMENT,
	Url TEXT NOT NULL,
	RawContent TEXT NOT NULL, 
	RunSentiment BOOLEAN NOT NULL,
	RunWhere TEXT NOT NULL, 
	RunWho TEXT NOT NULL,
	RunWhat TEXT NOT NULL,
	RunSummary TEXT NOT NULL,
	PRIMARY KEY (HitLinkID)	
);

CREATE TABLE QueryTable (
	Email varchar(255) NOT NULL,
	QueryID INT NOT NULL,
	FOREIGN KEY (Email) REFERENCES User(Email),
	FOREIGN KEY (QueryID) REFERENCES Query(QueryID) ON DELETE CASCADE,
	PRIMARY KEY (Email, QueryID)
);

CREATE TABLE ReferenceLinkTable (
	QueryID INT NOT NULL,
	ReferenceLinkID INT NOT NULL,
	FOREIGN KEY (QueryID) REFERENCES Query(QueryID),
	FOREIGN KEY (ReferenceLinkID) REFERENCES ReferenceLink(ReferenceLinkID) ON DELETE CASCADE,
	Primary Key (QueryID, ReferenceLinkID)
);

CREATE TABLE HitLinkTable (
	HitLinkID INT NOT NULL,
	ReferenceLinkID INT NOT NULL,
	FOREIGN KEY (ReferenceLinkID) REFERENCES ReferenceLink(ReferenceLinkID),
	FOREIGN KEY (HitLinkID) REFERENCES HitLink(HitLinkID) ON DELETE CASCADE,
	Primary Key (HitLinkID, ReferenceLinkID)
);
