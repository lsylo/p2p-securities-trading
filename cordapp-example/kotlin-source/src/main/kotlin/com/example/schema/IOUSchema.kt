package com.example.schema

import net.corda.core.schemas.MappedSchema
import net.corda.core.schemas.PersistentState
import java.util.*
import javax.persistence.Column
import javax.persistence.Entity
import javax.persistence.Table

/**
 * The family of schemas for BondState.
 */
object BondSchema

/**
 * An BondState schema.
 */
object BondSchemaV1 : MappedSchema(
        schemaFamily = BondSchema.javaClass,
        version = 1,
        mappedTypes = listOf(PersistentBond::class.java)) {
    @Entity
    @Table(name = "bond_states")
    class PersistentBond(
            @Column(name = "FaceValue")
            var FaceValue: Int,

            @Column(name = "CouponRate")
            var couponRate: Int,

            @Column(name = "Issuer")
            var Issuer: String,

            @Column(name = "Owner")
            var Owner: String,

            @Column(name = "CouponDates")
            var CouponDates: String,

            @Column(name = "MaturityDate")
            var MaturityDate: String,

            @Column(name = "linear_id")
            var linearId: UUID
    ) : PersistentState() {
        // Default constructor required by hibernate.
        constructor(): this("", "", 0, UUID.randomUUID())
    }
}