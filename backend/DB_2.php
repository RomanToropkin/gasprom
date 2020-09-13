<?php
/**
 * Created by PhpStorm.
 * User: FranQ
 * Date: 11.10.2019
 * Time: 13:48
 */

require_once '../api/Models/User.php';
require_once '../libs/Mysql.php';
require_once '../libs/Statement.php';

use Mysql\Mysql;
use Model\User;

class DB_2
{
    private $host = '***';
    private $log = '***';
    private $pass = '***';
    private $db;
    private $data_in_page = 7;

    public $codes = [
        'fail' => -1,
        'good' => 0,
        'bad_user' => 1,
        'bad_pass' => 2,
        'bad_login' => 3
    ];

    function __construct()
    {
        try {
            $this->db = Mysql::create($this->host, $this->log, $this->pass)
                ->setDatabaseName("gasprom")
                ->setCharset('utf8');
        } catch (Exception $e) {
            echo $e;
        }
    }

    public function get_events($offset, $filter = [], $query_text = '', $order = 'date', $order_type = 'ASC')
    {
        switch ($order){
            case 'date':
                $order = 'e.date';
                break;
            case 'dist':
                $order = 'e.dist';
                break;
            case 'speed':
                $order = 'e.speed';
                break;
        }
        $offset = $this->data_in_page * ($offset - 1);
        if ($filter) {
            if ($query_text) {
                $sql = "SELECT SQL_CALC_FOUND_ROWS
  e.id,
  e.id_client,
  st.name,
  e.date,
  e.lat,
  e.lon,
  ROUND(e.dist,2) as dist,
  ROUND(e.speed,2) as speed
FROM events
  e
LEFT JOIN
  station_type st ON st.id = e.id_station_type
WHERE e.id_station_type IN(?ai) AND e.id_client = ?i
ORDER BY ?s ?s LIMIT ?i OFFSET ?i;";
                $res = $this->db->query($sql, $filter, $query_text, $order, $order_type, $this->data_in_page, $offset);
            } else {
                $sql = "SELECT SQL_CALC_FOUND_ROWS
  e.id,
  e.id_client,
  st.name,
  e.date,
  e.lat,
  e.lon,
  ROUND(e.dist,2) as dist,
  ROUND(e.speed,2) as speed
FROM events
  e
LEFT JOIN
  station_type st ON st.id = e.id_station_type
WHERE e.id_station_type IN(?ai)
ORDER BY
  ?s ?s LIMIT ?i OFFSET ?i;";
                $res = $this->db->query($sql, $filter, $order, $order_type, $this->data_in_page, $offset);
            }
        } else {
            if ($query_text) {
                $sql = "SELECT SQL_CALC_FOUND_ROWS
  e.id,
  e.id_client,
  st.name,
  e.date,
  e.lat,
  e.lon,
  ROUND(e.dist,2) as dist,
  ROUND(e.speed,2) as speed
FROM events
  e
LEFT JOIN
  station_type st ON st.id = e.id_station_type
WHERE e.id_client = ?i
ORDER BY
  ?s ?s LIMIT ?i OFFSET ?i;";
                $res = $this->db->query($sql, $query_text, $order, $order_type, $this->data_in_page, $offset);
            } else {
                $sql = "SELECT SQL_CALC_FOUND_ROWS
  e.id,
  e.id_client,
  st.name,
  e.date,
  e.lat,
  e.lon,
  ROUND(e.dist,2) as dist,
  ROUND(e.speed,2) as speed
FROM events
  e
LEFT JOIN
  station_type st ON st.id = e.id_station_type
ORDER BY
  ?s ?s LIMIT ?i OFFSET ?i;";
                $res = $this->db->query($sql, $order, $order_type, $this->data_in_page, $offset);
            }
        }
        $data = $res->fetch_assoc_array();
        foreach ($data as &$val) {
            $date = new DateTime();
            $date->setTimestamp($val['date']);
            $val['date'] = $date->format('d.m.Y H:i:s');
        }
        $page_count = $this->db->query("SELECT FOUND_ROWS() as count;")->fetch_assoc()['count'];
        return ['page_count' => ceil($page_count / $this->data_in_page) . '', 'data' => $data];
    }


}