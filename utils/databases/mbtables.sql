DROP TABLE IF EXISTS bind_views,blacklist_domain,blacklist_host,whitelist_host,whitelist_domain,view_sinkholes,org_info,tlist_domains,tlist_ips;

CREATE TABLE org_info ( org_id INT NOT NULL AUTO_INCREMENT, org_name VARCHAR(60) NOT NULL, org_contact VARCHAR(80) NOT NULL, alert_contact VARCHAR(80) NOT NULL, pwd VARCHAR(60) NOT NULL, PRIMARY KEY (org_id) ) ENGINE=InnoDB;

CREATE TABLE view_sinkholes ( sinkhole_id INT NOT NULL AUTO_INCREMENT, org_id INT NOT NULL, sh_fqdn VARCHAR(20) NOT NULL, sh_ip BIGINT NOT NULL,  sh_desc VARCHAR(80), PRIMARY KEY (sinkhole_id), FOREIGN KEY (org_id) REFERENCES org_info(org_id) ON UPDATE CASCADE ON DELETE NO ACTION ) ENGINE=INNODB;

CREATE TABLE bind_views ( view_id INT NOT NULL AUTO_INCREMENT, org_id INT NOT NULL, view_name VARCHAR(40) NOT NULL, def_sh_id INT NOT NULL, view_src_acl_ips VARCHAR(100) NOT NULL, description VARCHAR(80), PRIMARY KEY (view_ID), FOREIGN KEY (org_id) REFERENCES org_info(org_id) ON UPDATE CASCADE ON DELETE NO ACTION, FOREIGN KEY (def_sh_id) REFERENCES view_sinkholes(sinkhole_id) ON UPDATE CASCADE ON DELETE NO ACTION ) ENGINE=INNODB;

CREATE TABLE whitelist_host ( wlh_id INT NOT NULL AUTO_INCREMENT, org_id INT NOT NULL,wlh_type VARCHAR(4) NOT NULL, wl_host VARCHAR(255), wlh_ip BIGINT ,  description VARCHAR(80), wlh_date DATE,  PRIMARY KEY (wlh_id), FOREIGN KEY (org_id) REFERENCES org_info(org_id) ON UPDATE CASCADE ON DELETE NO ACTION ) ENGINE=INNODB;

CREATE TABLE whitelist_domain ( wld_id INT NOT NULL AUTO_INCREMENT, org_id INT NOT NULL,wl_domain VARCHAR(255) NOT NULL, description VARCHAR(80), wlh_date DATE,  PRIMARY KEY (wld_id), FOREIGN KEY (org_id) REFERENCES org_info(org_id) ON UPDATE CASCADE ON DELETE NO ACTION ) ENGINE=INNODB;

CREATE TABLE blacklist_host ( blh_id INT NOT NULL AUTO_INCREMENT, org_id INT NOT NULL, blh_type VARCHAR(4) NOT NULL, bl_host VARCHAR(300), blh_ip BIGINT, blh_sinkhole INT NOT NULL, description VARCHAR(80), blh_date DATE, PRIMARY KEY (blh_id), FOREIGN KEY (org_id) REFERENCES org_info(org_id) ON UPDATE CASCADE ON DELETE NO ACTION,  FOREIGN KEY (blh_sinkhole) REFERENCES view_sinkholes(sinkhole_id) ON UPDATE CASCADE ON DELETE NO ACTION ) ENGINE=INNODB;

CREATE TABLE blacklist_domain ( bld_id INT NOT NULL AUTO_INCREMENT, org_id INT NOT NULL,bl_domain VARCHAR(300) NOT NULL, blh_sinkhole INT NOT NULL, description VARCHAR(80), blh_date DATE,  PRIMARY KEY (bld_id), FOREIGN KEY (org_id) REFERENCES org_info(org_id) ON UPDATE CASCADE ON DELETE NO ACTION, FOREIGN KEY (blh_sinkhole) REFERENCES view_sinkholes(sinkhole_id) ON UPDATE CASCADE ON DELETE NO ACTION ) ENGINE=INNODB;

CREATE TABLE tlist_domains (domain VARCHAR(300), PRIMARY KEY(domain)) ENGINE=INNODB;

CREATE TABLE tlist_ips (ip BIGINT, PRIMARY KEY(ip)) ENGINE=INNODB;