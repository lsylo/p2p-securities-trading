package com.example.state

import com.example.schema.IOUSchemaV1
import net.corda.core.contracts.ContractState
import net.corda.core.contracts.LinearState
import net.corda.core.contracts.UniqueIdentifier
import net.corda.core.identity.AbstractParty
import net.corda.core.identity.Party
import net.corda.core.schemas.MappedSchema
import net.corda.core.schemas.PersistentState
import net.corda.core.schemas.QueryableState

/**
 * The state object recording IOU agreements between two parties.
 *
 * A state must implement [ContractState] or one of its descendants.
 *
 * @param FaceValue the par value of the bond.
 * @param CouponRate the interest rate of the bond
 * @param Issuer the party who originally issued the bond.
 * @param Owner the current owner of the bond.
 * @param CouponDates the list of coupon payment dates.
 * @param MaturityDate the date at which bond matures.
 */
data class BondState(val FaceValue: Int,
                    val CouponRate: Int,
                    val Issuer: Party,
                    val Owner: Party,
                    CouponDates: Array,
                    MaturityDate: String,
                    override val linearId: UniqueIdentifier = UniqueIdentifier()):
        LinearState, QueryableState {
    /** The public keys of the involved parties. */
    override val participants: List<AbstractParty> get() = listOf(Issuer, Owner)

    override fun generateMappedObject(schema: MappedSchema): PersistentState {
        return when (schema) {
            is BondSchemaV1 -> BondSchemaV1.PersistentBond(
                    this.lender.name.toString(),
                    this.borrower.name.toString(),
                    this.value,
                    this.linearId.id
            )
            else -> throw IllegalArgumentException("Unrecognised schema $schema")
        }
    }

    override fun supportedSchemas(): Iterable<MappedSchema> = listOf(BondSchemaV1)
}
