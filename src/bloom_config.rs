use lazy_static::lazy_static;
use std::sync::atomic::AtomicI64;

pub const BLOOM_MAX_ITEM_COUNT_DEFAULT: i64 = 100000;
pub const BLOOM_MAX_ITEM_COUNT_MIN: i64 = 1;
pub const BLOOM_MAX_ITEM_COUNT_MAX: i64 = usize::MAX as i64;

pub const BLOOM_EXPANSION_DEFAULT: i64 = 2;
pub const BLOOM_EXPANSION_MIN: i64 = 1;
pub const BLOOM_EXPANSION_MAX: i64 = usize::MAX as i64;

lazy_static! {
    pub static ref BLOOM_MAX_ITEM_COUNT: AtomicI64 = AtomicI64::new(BLOOM_MAX_ITEM_COUNT_DEFAULT);
    pub static ref BLOOM_EXPANSION: AtomicI64 = AtomicI64::new(BLOOM_EXPANSION_DEFAULT);
}